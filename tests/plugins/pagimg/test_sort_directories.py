from pathlib import Path

from plugins.pagimg.navigation import sort_directories
from tests.temp import get_temporary_directory


def test_empty():
    directory_and_text = sort_directories([])
    assert directory_and_text == []


def test_lexicographic():
    with get_temporary_directory() as temporary_directory:
        paths = [
            Path(temporary_directory, "aa_aaa aa"),
            Path(temporary_directory, "cc_ccc cc"),
            Path(temporary_directory, "bb_bbb bb")
        ]
        for path in paths:
            path.mkdir()
        directory_and_text = sort_directories(paths)
        assert directory_and_text[0] == (paths[0], "Aa Aaa Aa")
        assert directory_and_text[1] == (paths[2], "Bb Bbb Bb")
        assert directory_and_text[2] == (paths[1], "Cc Ccc Cc")


def test_numeric():
    with get_temporary_directory() as temporary_directory:
        paths = [
            Path(temporary_directory, "3_aa_aaa aa"),
            Path(temporary_directory, "1_cc_ccc cc"),
            Path(temporary_directory, "2_bb_bbb bb")
        ]
        for path in paths:
            path.mkdir()
        directory_and_text = sort_directories(paths)
        assert directory_and_text[0] == (paths[1], "Cc Ccc Cc")
        assert directory_and_text[1] == (paths[2], "Bb Bbb Bb")
        assert directory_and_text[2] == (paths[0], "Aa Aaa Aa")
