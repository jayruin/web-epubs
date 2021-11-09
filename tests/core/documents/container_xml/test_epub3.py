from pathlib import Path

from core.documents import ContainerXML
from tests.temp import get_temporary_file


def test_no_sep():
    parent_directory = Path(__file__).parent
    package_document = Path("package.opf")
    document = ContainerXML(package_document)
    with get_temporary_file() as actual_file:
        document.epub3(actual_file)
        expected_file = Path(parent_directory, "expected", "no_sep.xml")
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        assert actual == expected


def test_sep():
    parent_directory = Path(__file__).parent
    package_document = Path("OEBPS/package.opf")
    document = ContainerXML(package_document)
    with get_temporary_file() as actual_file:
        document.epub3(actual_file)
        expected_file = Path(parent_directory, "expected", "sep.xml")
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        assert actual == expected
