from pathlib import Path

from core.documents import NavigationDocument
from tests.core.documents.shared import check_epub2_document


def test_no_landmarks(
    navigation_document_no_landmarks: NavigationDocument,
    expected_file_epub2_no_landmarks: Path
):
    assert check_epub2_document(
        navigation_document_no_landmarks,
        expected_file_epub2_no_landmarks
    )


def test_empty_landmarks(
    navigation_document_empty_landmarks: NavigationDocument,
    expected_file_epub2_no_landmarks: Path
):
    assert check_epub2_document(
        navigation_document_empty_landmarks,
        expected_file_epub2_no_landmarks
    )


def test_nonempty_landmarks(
    navigation_document_nonempty_landmarks: NavigationDocument,
    expected_file_epub2_no_landmarks: Path
):
    assert check_epub2_document(
        navigation_document_nonempty_landmarks,
        expected_file_epub2_no_landmarks
    )
