from __future__ import annotations
from typing import TYPE_CHECKING

from lxml import etree

from . import shared

if TYPE_CHECKING:
    from core.datastructures import Tree
    from core.project import Anchor


def make_body_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    body = etree.Element("body")

    h1 = etree.Element("h1")
    h1.text = "Navigation"
    body.append(h1)

    ol = shared.make_ol_element(nav_trees)
    body.append(ol)

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
