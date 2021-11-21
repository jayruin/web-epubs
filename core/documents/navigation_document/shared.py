from lxml import etree

from core.datastructures import Tree
from core.project import Anchor


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


CSS_STYLE = """
            a {
                text-decoration: none;
            }
        """
