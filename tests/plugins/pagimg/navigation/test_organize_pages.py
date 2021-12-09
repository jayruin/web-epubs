from pathlib import Path

from plugins.pagimg.navigation import organize_pages
from tests.temp import get_temporary_directory


def test_empty():
    with get_temporary_directory() as directory:
        assert organize_pages(directory, directory) is None


def test_no_pages():
    with get_temporary_directory() as directory:
        Path(directory, "empty1").mkdir()
        Path(directory, "empty2").mkdir()
        Path(directory, "empty3").mkdir()
        assert organize_pages(directory, directory) is None


def test_has_pages():
    with get_temporary_directory() as directory:
        pages = [Path(directory, f"{str(i)}.jpg") for i in range(1, 4)]
        for page in pages:
            page.touch()
        tree = organize_pages(directory, directory)
        assert tree is not None
        assert tree.value.pages == pages


def test_first_page_of_first_child():
    with get_temporary_directory() as directory:
        child_directory = Path(directory, "child_with_pages")
        child_directory.mkdir()
        pages = [Path(child_directory, f"{str(i)}.jpg") for i in range(1, 4)]
        for page in pages:
            page.touch()
        tree = organize_pages(directory, directory)
        assert tree is not None
        assert len(tree.value.pages) == 0
        assert tree.value.href == tree.children[0].value.href


def test_href():
    with get_temporary_directory() as directory:
        pages = [Path(directory, f"{str(i)}.jpg") for i in range(1, 4)]
        for page in pages:
            page.touch()
        tree = organize_pages(directory, directory)
        assert tree is not None
        actual_href = tree.value.href
        expected_href = pages[0].relative_to(directory).with_suffix(".xhtml")
        assert actual_href == expected_href


def test_recursive():
    with get_temporary_directory() as directory:
        subdirectories = [
            Path(directory, f"subdirectory{str(i)}")
            for i in range(1, 3)
        ]
        for i, subdirectory in enumerate(subdirectories):
            subdirectory.mkdir()
            pages = [
                Path(subdirectory, f"{str(j + i * 3)}.jpg")
                for j in range(1, 4)
            ]
            for page in pages:
                page.touch()
        tree = organize_pages(directory, directory)
        assert tree is not None
        for i, subdirectory in enumerate(subdirectories):
            child = tree.children[i]
            assert child.value.href == Path(
                f"subdirectory{str(i + 1)}",
                f"{str(1 + i * 3)}.xhtml"
            )
            assert child.value.pages == [
                Path(subdirectory, f"{str(j + i * 3)}.jpg")
                for j in range(1, 4)
            ]
            assert child.children == []


def test_text():
    with get_temporary_directory() as directory:
        Path(directory, "A").mkdir()
        Path(directory, "B").mkdir()
        Path(directory, "A", "C").mkdir()
        Path(directory, "A", "D").mkdir()
        Path(directory, "B", "E").mkdir()
        Path(directory, "B", "F").mkdir()
        Path(directory, "A", "C", "1.jpg").touch()
        Path(directory, "A", "D", "1.jpg").touch()
        Path(directory, "B", "E", "1.jpg").touch()
        Path(directory, "B", "F", "1.jpg").touch()
        tree = organize_pages(directory, directory)
        assert tree is not None
        assert len(tree.children) == 2
        assert tree.children[0].value.text == "A"
        assert tree.children[1].value.text == "B"
        assert len(tree.children[0].children) == 2
        assert tree.children[0].children[0].value.text == "C"
        assert tree.children[0].children[1].value.text == "D"
        assert len(tree.children[1].children) == 2
        assert tree.children[1].children[0].value.text == "E"
        assert tree.children[1].children[1].value.text == "F"
