from __future__ import annotations
from typing import TYPE_CHECKING

from tests.core.documents.shared import check_epub2_document

if TYPE_CHECKING:
    from pathlib import Path

    from core.documents import EPUB2PackageDocument


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
