from pathlib import Path

from core.documents import MimetypeFile
from tests.temp import get_temporary_file


def test_mimetype_file():
    parent_directory = Path(__file__).parent
    document = MimetypeFile()
    with get_temporary_file() as actual_file:
        document.epub2(actual_file)
        expected_file = Path(parent_directory, "expected", "mimetype")
        actual = actual_file.read_bytes()
        expected = expected_file.read_bytes()
        assert actual == expected
