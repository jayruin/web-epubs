from __future__ import annotations
from typing import TYPE_CHECKING

from lxml import etree

from core.templates import EPUB3Template

if TYPE_CHECKING:
    from pathlib import Path


def make_html_element(width: int, height: int, src: Path) -> etree._Element:
    template = EPUB3Template([], [])
    html = template.generate_root_element("Paginated Image")

    head = html.find("head")
    assert head is not None
    meta_viewport = make_meta_viewport_element(width, height)
    head.append(meta_viewport)

    body = make_body_element(src)
    html.append(body)

    return html


def make_meta_viewport_element(
    width: int,
    height: int
) -> etree._Element:
    meta = etree.Element(
        "meta",
        attrib={
            "name": "viewport",
            "content": f"width={width}, height={height}"
        }
    )
    return meta


def make_body_element(src: Path) -> etree._Element:
    body = etree.Element("body")

    img = etree.Element(
        "img",
        attrib={
            "src": src.as_posix()
        }
    )
    body.append(img)

    return body
