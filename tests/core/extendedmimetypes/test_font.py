from core.extendedmimetypes import mimetypes


def test_otf():
    actual = mimetypes.guess_type("otf.otf")[0]
    expected = "font/otf"
    assert actual == expected


def test_ttf():
    actual = mimetypes.guess_type("ttf.ttf")[0]
    expected = "font/ttf"
    assert actual == expected


def test_woff():
    actual = mimetypes.guess_type("woff.woff")[0]
    expected = "font/woff"
    assert actual == expected


def test_woff2():
    actual = mimetypes.guess_type("woff2.woff2")[0]
    expected = "font/woff2"
    assert actual == expected
