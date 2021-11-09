from core.extendedmimetypes import mimetypes


def test_css():
    actual = mimetypes.guess_type("css.css")[0]
    expected = "text/css"
    assert actual == expected
