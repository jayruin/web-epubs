from pathlib import Path

from plugins.pagimg.navigation import sort_files


def test_empty():
    sorted_files = sort_files([])
    assert sorted_files == []


def test_lexicographic():
    paths = [
        Path("9c.txt"),
        Path("b.txt"),
        Path("a.txt")
    ]
    sorted_files = sort_files(paths)
    assert sorted_files[0] == paths[0]
    assert sorted_files[1] == paths[2]
    assert sorted_files[2] == paths[1]


def test_numeric():
    paths = [
        Path("10.txt"),
        Path("1.txt"),
        Path("5.txt")
    ]
    sorted_files = sort_files(paths)
    assert sorted_files[0] == paths[1]
    assert sorted_files[1] == paths[2]
    assert sorted_files[2] == paths[0]
