from __future__ import annotations
from functools import partial
import json
from pathlib import Path
from typing import Any, cast, TYPE_CHECKING

from lxml import etree
import yaml

from core.constants import Encoding, INDENT
if TYPE_CHECKING:
    from core.project.anchor import Anchor
    from core.project.nav_dict import NavDict
    from core.project.tree import Tree


def get_dump(suffix: str) -> Any:
    match suffix:
        case ".json":
            dump = partial(
                cast(Any, json).dump,
                ensure_ascii=False,
                indent=4
            )
        case ".yaml" | ".yml":
            dump = partial(
                cast(Any, yaml).dump,
                allow_unicode=True,
                indent=2,
                sort_keys=False
            )
        case _:
            raise ValueError(f"{suffix} is unsupported for metadata!")
    return dump


def tree_to_nav_dict(tree: Tree[Anchor]) -> NavDict:
    return {
        "text": tree.value.text,
        "href": tree.value.href.as_posix(),
        "children": [tree_to_nav_dict(child) for child in tree.children]
    }


def write_nav(path: Path, nav: list[Tree[Anchor]]) -> None:
    dump = get_dump(path.suffix)
    with open(path, "w", encoding=Encoding.UTF_8.value) as f:
        dump([tree_to_nav_dict(tree) for tree in nav], f)


def get_doctype_html(include_dtd: bool) -> str:
    if include_dtd:
        dtd = " " + " ".join(
            [
                "PUBLIC",
                "\"-//W3C//DTD XHTML 1.1//EN\"",
                "\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\""
            ]
        )
    else:
        dtd = ""
    return f"<!DOCTYPE html{dtd}>"


def get_xml_header(encoding: str) -> str:
    return f"<?xml version=\"1.0\" encoding=\"{encoding}\"?>"


def write_epub3_xhtml_element(
    root_element: etree._Element,
    path: Path,
    indent: bool = True
) -> None:
    if indent:
        etree.indent(root_element, space=INDENT)
    with open(path, "wb") as f:
        f.write(
            etree.tostring(
                root_element,
                encoding=Encoding.UTF_8.value,
                doctype="\n".join(
                    [
                        get_xml_header(Encoding.UTF_8.value),
                        get_doctype_html(include_dtd=False)
                    ]
                )
            )
        )


def write_epub2_xhtml_element(
    root_element: etree._Element,
    path: Path,
    indent: bool = True
) -> None:
    if indent:
        etree.indent(root_element, space=INDENT)
    with open(path, "wb") as f:
        f.write(
            etree.tostring(
                root_element,
                encoding=Encoding.UTF_8.value,
                doctype="\n".join(
                    [
                        get_xml_header(Encoding.UTF_8.value),
                        get_doctype_html(include_dtd=True)
                    ]
                )
            )
        )


def write_xml_element(
    root_element: etree._Element,
    path: Path,
    indent: bool = True
) -> None:
    if indent:
        etree.indent(root_element, space=INDENT)
    with open(path, "wb") as f:
        f.write(
            etree.tostring(
                root_element,
                encoding=Encoding.UTF_8.value,
                doctype=get_xml_header(Encoding.UTF_8.value)
            )
        )
