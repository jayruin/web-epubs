from pathlib import Path

from plugins.pagimg.navigation import sort_directories


def test_empty():
    directory_and_text = sort_directories([])
    assert directory_and_text == []


def test_lexicographic():
    paths = [
        Path("aa_aaa aa"),
        Path("cc_ccc cc"),
        Path("bb_bbb bb")
    ]
    directory_and_text = sort_directories(paths)
    assert directory_and_text[0] == (paths[0], "Aa Aaa Aa")
    assert directory_and_text[1] == (paths[2], "Bb Bbb Bb")
    assert directory_and_text[2] == (paths[1], "Cc Ccc Cc")


def test_numeric():
    paths = [
        Path("3_aa_aaa aa"),
        Path("1_cc_ccc cc"),
        Path("2_bb_bbb bb")
    ]
    directory_and_text = sort_directories(paths)
    assert directory_and_text[0] == (paths[1], "Cc Ccc Cc")
    assert directory_and_text[1] == (paths[2], "Bb Bbb Bb")
    assert directory_and_text[2] == (paths[0], "Aa Aaa Aa")
