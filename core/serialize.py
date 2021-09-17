from pathlib import Path
from lxml import etree
from lxml.etree import _Element as Element

from core.constants import Encoding, INDENT


def get_doctype_html(include_dtd: bool) -> str:
    if include_dtd:
        dtd = " ".join(
            [
                "\"-//W3C//DTD XHTML 1.1//EN\"",
                "\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\""
            ]
        )
    else:
        dtd = ""
    return f"<!DOCTYPE html{dtd}>"


def get_xml_header(encoding: str) -> str:
    return f"<?xml version=\"1.0\" encoding=\"{encoding}\"?>"


def write_epub3_xhtml_element(root_element: Element, path: Path) -> None:
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


def write_epub2_xhtml_element(root_element: Element, path: Path) -> None:
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
