from __future__ import annotations
from typing import TYPE_CHECKING

from lxml import etree

from . import shared

if TYPE_CHECKING:
    from pathlib import Path


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
