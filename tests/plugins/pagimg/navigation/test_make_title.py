from plugins.pagimg.navigation import make_title


def test_all_caps():
    text = "AAA"
    assert text == make_title(text)


def test_mostly_caps():
    text = "aBC"
    expected = "ABC"
    assert expected == make_title(text)


def test_apostrophe():
    text = "i'm testing"
    expected = "I'm Testing"
    assert expected == make_title(text)


def test_starts_with_int():
    text = "1test"
    assert text == make_title(text)


def test_multiple_spaces():
    text = "a   word"
    expected = "A   Word"
    assert expected == make_title(text)
