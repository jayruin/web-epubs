from core.extendedmimetypes import mimetypes


def test_js():
    actual = mimetypes.guess_type("js.js")[0]
    expected = "application/javascript"
    assert actual == expected


def test_ncx():
    actual = mimetypes.guess_type("ncx.ncx")[0]
    expected = "application/x-dtbncx+xml"
    assert actual == expected


def test_xhtml():
    actual = mimetypes.guess_type("xhtml.xhtml")[0]
    expected = "application/xhtml+xml"
    assert actual == expected
