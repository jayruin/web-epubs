from lxml import etree

from . import shared
from core.datastructures import Tree
from core.project import Anchor
from core.templates import EPUB2Template


def make_html_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    template = EPUB2Template([])
    html = template.generate_root_element("Navigation")

    head = html.find("head")
    assert head is not None
    style = make_style_element()
    head.append(style)

    body = make_body_element(nav_trees)
    html.append(body)

    return html


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
