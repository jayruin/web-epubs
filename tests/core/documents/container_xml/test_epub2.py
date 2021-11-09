from pathlib import Path

from core.documents import ContainerXML
from tests.core.documents.shared import check_epub2_document


def test_no_sep():
    parent_directory = Path(__file__).parent
    package_document = Path("package.opf")
    document = ContainerXML(package_document)
    expected_file = Path(parent_directory, "expected", "no_sep.xml")
    assert check_epub2_document(document, expected_file)


def test_sep():
    parent_directory = Path(__file__).parent
    package_document = Path("OEBPS/package.opf")
    document = ContainerXML(package_document)
    expected_file = Path(parent_directory, "expected", "sep.xml")
    assert check_epub2_document(document, expected_file)
