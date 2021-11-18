from pathlib import Path

from core.documents.abcs import EPUB3Document, EPUB2Document
from tests.temp import get_temporary_file


def check_epub2_document(document: EPUB2Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.write_epub2(actual_file)
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        return actual == expected


def check_epub3_document(document: EPUB3Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.write_epub3(actual_file)
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        return actual == expected
