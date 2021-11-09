from pathlib import Path

from core.documents import MimetypeFile
from tests.core.documents.shared import check_epub3_document


def test_mimetype_file():
    parent_directory = Path(__file__).parent
    document = MimetypeFile()
    expected_file = Path(parent_directory, "expected", "mimetype")
    assert check_epub3_document(document, expected_file)
