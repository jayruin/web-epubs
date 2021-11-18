from __future__ import annotations
from typing import TYPE_CHECKING

from lxml import etree

from . import shared
from core.constants import Namespace

if TYPE_CHECKING:
    from typing import Optional

    from core.datastructures import Tree
    from core.project import Anchor, TypedAnchor


def make_body_element(
    nav_trees: list[Tree[Anchor]],
    landmarks: Optional[list[TypedAnchor]] = None
) -> etree._Element:
    body = etree.Element("body")

    section = etree.Element(
        "section",
        attrib={
            etree.QName(Namespace.EPUB.value, "type"): "bodymatter chapter"
        }
    )
    body.append(section)

    h1 = etree.Element("h1")
    h1.text = "Navigation"
    section.append(h1)

    toc_nav = make_toc_element(nav_trees)
    section.append(toc_nav)

    if landmarks:
        landmarks_nav = make_landmarks_element(landmarks)
        section.append(landmarks_nav)

    return body


def make_toc_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    nav = etree.Element(
        "nav",
        attrib={
            etree.QName(Namespace.EPUB.value, "type"): "toc"
        }
    )

    h2 = etree.Element("h2")
    h2.text = "Table of Contents"
    nav.append(h2)

    ol = shared.make_ol_element(nav_trees)
    nav.append(ol)

    return nav


def make_landmarks_element(
    landmarks: list[TypedAnchor]
) -> etree._Element:
    nav = etree.Element(
        "nav",
        attrib={
            etree.QName(Namespace.EPUB.value, "type"): "landmarks",
            "hidden": "hidden"
        }
    )

    h2 = etree.Element("h2")
    h2.text = "Landmarks"
    nav.append(h2)

    ol = etree.Element("ol")
    nav.append(ol)

    for anchor in landmarks:
        assert anchor.type

        li = etree.Element("li")
        ol.append(li)

        a = etree.Element(
            "a",
            attrib={
                etree.QName(Namespace.EPUB.value, "type"): anchor.type,
                "href": anchor.href.as_posix()
            }
        )
        a.text = anchor.text
        li.append(a)

    return nav


def make_style_element() -> etree._Element:
    style = etree.Element("style")
    style.text = shared.CSS_STYLE
    return style
