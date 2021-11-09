from pathlib import Path

from core.documents import EPUB2Document, EPUB3Document
from tests.temp import get_temporary_file


def check_epub2_document(document: EPUB2Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.epub2(actual_file)
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        return actual == expected


def check_epub3_document(document: EPUB3Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.epub3(actual_file)
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        return actual == expected
