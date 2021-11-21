from pathlib import Path

from core.documents import CoverXHTML
from tests.core.documents.shared import check_epub2_document


def test_no_sep(
    cover_xhtml_no_sep: CoverXHTML,
    expected_file_epub2_no_sep: Path
):
    assert check_epub2_document(cover_xhtml_no_sep, expected_file_epub2_no_sep)


def test_sep(cover_xhtml_sep: CoverXHTML, expected_file_epub2_sep: Path):
    assert check_epub2_document(cover_xhtml_sep, expected_file_epub2_sep)
