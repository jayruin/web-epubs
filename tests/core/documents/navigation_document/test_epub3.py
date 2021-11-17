from __future__ import annotations
from typing import TYPE_CHECKING

from tests.core.documents.shared import check_epub3_document

if TYPE_CHECKING:
    from pathlib import Path

    from core.documents import NavigationDocument


def test_no_landmarks(
    navigation_document_no_landmarks: NavigationDocument,
    expected_file_epub3_no_landmarks: Path
):
    assert check_epub3_document(
        navigation_document_no_landmarks,
        expected_file_epub3_no_landmarks
    )


def test_empty_landmarks(
    navigation_document_empty_landmarks: NavigationDocument,
    expected_file_epub3_no_landmarks: Path
):
    assert check_epub3_document(
        navigation_document_empty_landmarks,
        expected_file_epub3_no_landmarks
    )


def test_nonempty_landmarks(
    navigation_document_nonempty_landmarks: NavigationDocument,
    expected_file_epub3_nonempty_landmarks: Path
):
    assert check_epub3_document(
        navigation_document_nonempty_landmarks,
        expected_file_epub3_nonempty_landmarks
    )
