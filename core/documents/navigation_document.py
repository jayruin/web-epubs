from pathlib import Path
from typing import Optional

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import Namespace
from core.project import Anchor, Tree
from core.serialize import write_epub3_xhtml_element
from core.templates import EPUB3Template


class NavigationDocument(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the EPUB Navigation Document.
    May also be used as an inline table of contents.
    """
    def __init__(
        self,
        nav_trees: list[Tree[Anchor]],
        css_files: list[Path],
        landmarks: Optional[list[Anchor]] = None
    ) -> None:
        self.nav_trees = nav_trees
        self.css_files = css_files
        self.landmarks = landmarks

    def epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-nav
        """
        template = EPUB3Template(self.css_files, [])
        html = template.generate_root_element("Navigation")

        body = make_epub3_body_element(self.nav_trees, self.landmarks)
        html.append(body)

        write_epub3_xhtml_element(html, path)

    def epub2(self, path: Path) -> None:
        pass


def make_li_element(nav_tree: Tree[Anchor]) -> etree._Element:
    li = etree.Element("li")
    a = etree.Element(
        "a",
        attrib={
            "href": nav_tree.value.href.as_posix()
        }
    )
    a.text = nav_tree.value.text
    li.append(a)

    if nav_tree.children:
        ol = etree.Element("ol")
        li.append(ol)
        for child in nav_tree.children:
            ol.append(make_li_element(child))

    return li


def make_ol_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    ol = etree.Element("ol")

    for nav_tree in nav_trees:
        ol.append(make_li_element(nav_tree))

    return ol


def make_epub3_body_element(
    nav_trees: list[Tree[Anchor]],
    landmarks: Optional[list[Anchor]] = None
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

    toc_nav = make_epub3_toc_element(nav_trees)
    section.append(toc_nav)

    if landmarks is not None:
        landmarks_nav = make_epub3_landmarks_element(landmarks)
        section.append(landmarks_nav)

    return body


def make_epub3_toc_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    nav = etree.Element(
        "nav",
        attrib={
            etree.QName(Namespace.EPUB.value, "type"): "toc"
        }
    )

    h2 = etree.Element("h2")
    h2.text = "Table of Contents"
    nav.append(h2)

    ol = make_ol_element(nav_trees)
    nav.append(ol)

    return nav


def make_epub3_landmarks_element(landmarks: list[Anchor]) -> etree._Element:
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
