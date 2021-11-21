from pathlib import Path

from core.documents import NCXDocument
from tests.core.documents.shared import check_epub2_document


def test_empty_nav_trees(
    ncx_document_empty_nav_trees: NCXDocument,
    expected_file_empty_nav_trees: Path
):
    assert check_epub2_document(
        ncx_document_empty_nav_trees,
        expected_file_empty_nav_trees
    )


def test_nonempty_nav_trees(
    ncx_document_nonempty_nav_trees: NCXDocument,
    expected_file_nonempty_nav_trees: Path
):
    assert check_epub2_document(
        ncx_document_nonempty_nav_trees,
        expected_file_nonempty_nav_trees
    )
