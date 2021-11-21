from pathlib import Path

from lxml import etree

from . import shared
from core.templates import EPUB2Template


def make_html_element(cover_file: Path) -> etree._Element:
    template = EPUB2Template([])
    html = template.generate_root_element("Cover")

    head = html.find("head")
    assert head is not None
    style = make_style_element()
    head.append(style)

    body = make_body_element(cover_file)
    html.append(body)

    return html


def make_body_element(cover_file: Path) -> etree._Element:
    body = etree.Element("body")

    div = etree.Element(
        "div",
        attrib={
            "class": "cover-container"
        }
    )
    body.append(div)

    img = etree.Element(
        "img",
        attrib={
            "alt": "Cover",
            "src": cover_file.as_posix()
        }
    )
    div.append(img)

    return body


def make_style_element() -> etree._Element:
    style = etree.Element(
        "style",
        attrib={
            "type": "text/css"
        }
    )
    style.text = shared.CSS_STYLE
    return style
