from pathlib import Path

from core.documents import EPUB3PackageDocument
from tests.core.documents.shared import check_epub3_document


def test_minimal(
    epub3_package_document_minimal: EPUB3PackageDocument,
    expected_file_epub3_minimal: Path
):
    assert check_epub3_document(
        epub3_package_document_minimal,
        expected_file_epub3_minimal
    )


def test_empty_landmarks(
    epub3_package_document_maximal: EPUB3PackageDocument,
    expected_file_epub3_maximal: Path
):
    assert check_epub3_document(
        epub3_package_document_maximal,
        expected_file_epub3_maximal
    )
