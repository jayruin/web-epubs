from pathlib import Path

from core.documents import EPUB2PackageDocument
from tests.core.documents.shared import check_epub2_document


def test_no_landmarks(
    epub2_package_document_no_landmarks: EPUB2PackageDocument,
    expected_file_epub2_no_landmarks: Path
):
    assert check_epub2_document(
        epub2_package_document_no_landmarks,
        expected_file_epub2_no_landmarks
    )


def test_empty_landmarks(
    epub2_package_document_empty_landmarks: EPUB2PackageDocument,
    expected_file_epub2_no_landmarks: Path
):
    assert check_epub2_document(
        epub2_package_document_empty_landmarks,
        expected_file_epub2_no_landmarks
    )


def test_nonempty_landmarks(
    epub2_package_document_nonempty_landmarks: EPUB2PackageDocument,
    expected_file_epub2_nonempty_landmarks: Path
):
    assert check_epub2_document(
        epub2_package_document_nonempty_landmarks,
        expected_file_epub2_nonempty_landmarks
    )
