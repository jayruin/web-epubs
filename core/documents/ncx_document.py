from pathlib import Path

from lxml import etree

from .epub2document import EPUB2Document
from core.constants import Namespace
from core.datastructures import Tree
from core.project import Anchor
from core.serialize import write_xml_element


class NCXDocument(EPUB2Document):
    """
    An XML document corresponding to the Navigation Center eXtended.
    """
    def __init__(
        self, nav_trees: list[Tree[Anchor]],
        identifier: str,
        title: str
    ) -> None:
        self.nav_trees = nav_trees
        self.identifier = identifier
        self.title = title

    def epub2(self, path: Path) -> None:
        """
        http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1
        """
        ncx = make_ncx_element(self.nav_trees, self.identifier, self.title)

        write_xml_element(ncx, path)


def make_ncx_element(
    nav_trees: list[Tree[Anchor]],
    identifier: str,
    title: str
) -> etree._Element:
    ncx = etree.Element(
        "ncx",
        attrib={
            "version": "2005-1"
        },
        nsmap={
            None: Namespace.NCX.value
        }
    )

    head = make_head_element(identifier)
    ncx.append(head)

    doctitle = make_doctitle_element(title)
    ncx.append(doctitle)

    navmap = make_navmap_element(nav_trees)
    ncx.append(navmap)

    return ncx


def make_head_element(identifier: str) -> etree._Element:
    head = etree.Element("head")

    meta = etree.Element(
        "meta",
        attrib={
            "name": "dtb:uid",
            "content": identifier
        }
    )
    head.append(meta)

    return head


def make_doctitle_element(title: str) -> etree._Element:
    doctitle = etree.Element("docTitle")

    text = etree.Element("text")
    text.text = title
    doctitle.append(text)

    return doctitle


def make_navmap_element(nav_trees: list[Tree[Anchor]]) -> etree._Element:
    navmap = etree.Element("navMap")

    if len(nav_trees) == 0:
        navmap.text = ""
    for count, nav_tree in enumerate(nav_trees):
        navmap.append(make_navpoint_element(nav_tree, [count]))

    return navmap


def make_navpoint_element(
    nav_tree: Tree[Anchor], counts: list[int]
) -> etree._Element:
    navpoint = etree.Element(
        "navPoint",
        attrib={
            "id": "ncx-" + "-".join(str(count) for count in counts)
        }
    )

    navlabel = etree.Element("navLabel")
    navpoint.append(navlabel)

    text = etree.Element("text")
    text.text = nav_tree.value.text
    navlabel.append(text)

    content = etree.Element(
        "content",
        attrib={
            "src": nav_tree.value.href.as_posix()
        }
    )
    navpoint.append(content)

    for child_count, child in enumerate(nav_tree.children):
        navpoint.append(make_navpoint_element(child, [*counts, child_count]))
    return navpoint
