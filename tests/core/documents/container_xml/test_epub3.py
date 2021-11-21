from pathlib import Path

from core.documents import ContainerXML
from tests.core.documents.shared import check_epub3_document


def test_no_sep(
    container_xml_no_sep: ContainerXML,
    expected_file_no_sep: Path
):
    assert check_epub3_document(container_xml_no_sep, expected_file_no_sep)


def test_sep(container_xml_sep: ContainerXML, expected_file_sep: Path):
    assert check_epub3_document(container_xml_sep, expected_file_sep)
