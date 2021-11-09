from core.extendedmimetypes import mimetypes


def test_gif():
    actual = mimetypes.guess_type("gif.gif")[0]
    expected = "image/gif"
    assert actual == expected


def test_jpg():
    actual = mimetypes.guess_type("jpg.jpg")[0]
    expected = "image/jpeg"
    assert actual == expected


def test_png():
    actual = mimetypes.guess_type("png.png")[0]
    expected = "image/png"
    assert actual == expected


def test_svg():
    actual = mimetypes.guess_type("svg.svg")[0]
    expected = "image/svg+xml"
    assert actual == expected
