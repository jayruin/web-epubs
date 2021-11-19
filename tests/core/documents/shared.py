import difflib
from pathlib import Path
import sys

from core.constants import Encoding
from core.documents.abcs import EPUB3Document, EPUB2Document
from tests.temp import get_temporary_file


def compare_files(actual: Path, expected: Path) -> bool:
    with open(actual, "r", encoding=Encoding.UTF_8.value) as f:
        actual_lines = f.readlines()
    with open(expected, "r", encoding=Encoding.UTF_8.value) as f:
        expected_lines = f.readlines()
    delta = difflib.unified_diff(
        actual_lines,
        expected_lines,
        fromfile="actual",
        tofile="expected"
    )
    sys.stderr.writelines(delta)
    actual_bytes = actual.read_bytes()
    expected_bytes = expected.read_bytes()
    return actual_bytes == expected_bytes


def check_epub2_document(document: EPUB2Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.write_epub2(actual_file)
        return compare_files(actual_file, expected_file)


def check_epub3_document(document: EPUB3Document, expected_file: Path) -> bool:
    with get_temporary_file() as actual_file:
        document.write_epub3(actual_file)
        return compare_files(actual_file, expected_file)
