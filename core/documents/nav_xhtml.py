from pathlib import Path

from lxml import etree
from lxml.etree import _Element as Element

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import (
    DOCTYPE_HTML_EPUB3,
    # DOCTYPE_HTML_EPUB2,
    Encoding,
    INDENT,
    Namespace,
    XML_HEADER
)
from core.project import Anchor, Tree
from core.templates import EPUB3Template


def nav_tree_to_li(nav_tree: Tree[Anchor]) -> Element:
    li = etree.Element("li")
    a = etree.Element(
        "a",
        attrib={
            "href": nav_tree.value.href
        }
    )
    a.text = nav_tree.value.text
    li.append(a)

    if nav_tree.children:
        ol = etree.Element("ol")
        li.append(ol)
        for child in nav_tree.children:
            ol.append(nav_tree_to_li(child))

    return li


class NavXHTML(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the nav/toc file.
    """
    def __init__(
        self,
        nav_trees: list[Tree[Anchor]],
        css_files: list[Path]
    ) -> None:
        self.nav_trees = nav_trees
        self.css_files = css_files

    def epub3(self, path: Path) -> None:
        template = EPUB3Template(self.css_files, [])
        html = template.generate_root_element("Contents")
        body = html.find("body")
        assert body is not None

        section = etree.Element(
            "section",
            attrib={
                etree.QName(Namespace.EPUB.value, "type"): "bodymatter chapter"
            }
        )
        body.append(section)

        nav = etree.Element(
            "nav",
            attrib={
                etree.QName(Namespace.EPUB.value, "type"): "toc"
            }
        )
        section.append(nav)

        h1 = etree.Element("h1")
        h1.text = "Contents"
        nav.append(h1)

        ol = etree.Element(
            "ol",
            attrib={
                etree.QName(Namespace.EPUB.value, "type"): "list"
            }
        )
        nav.append(ol)

        for nav_tree in self.nav_trees:
            ol.append(nav_tree_to_li(nav_tree))

        etree.indent(html, space=INDENT)
        with open(path, "wb") as f:
            f.write(
                etree.tostring(
                    html,
                    encoding=Encoding.UTF_8.value,
                    doctype="\n".join([XML_HEADER, DOCTYPE_HTML_EPUB3])
                )
            )

    def epub2(self, path: Path) -> None:
        pass
