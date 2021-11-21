from pathlib import Path

from core.documents import MimetypeFile
from tests.core.documents.shared import check_epub2_document


def test_mimetype_file(mimetype_file: MimetypeFile, expected_file: Path):
    assert check_epub2_document(mimetype_file, expected_file)
