from pathlib import Path

from lxml import etree
from lxml.etree import _Element as Element

from .xhtml_template import XHTMLTemplate
from core.constants import (
    DOCTYPE_HTML_EPUB3,
    Encoding,
    INDENT,
    Namespace,
    XML_HEADER
)


def write_epub3_xhtml_element(root_element: Element, path: Path) -> None:
    etree.indent(root_element, space=INDENT)
    with open(path, "wb") as f:
        f.write(
            etree.tostring(
                root_element,
                encoding=Encoding.UTF_8.value,
                doctype="\n".join([XML_HEADER, DOCTYPE_HTML_EPUB3])
            )
        )


class EPUB3Template(XHTMLTemplate):
    """
    https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-xhtml
    Template for an EPUB3 XHTML content document.
    """
    def __init__(self, css_files: list[Path], js_files: list[Path]) -> None:
        self.css_files = css_files
        self.js_files = js_files

    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        pass

    def generate_root_element(self, title_text: str) -> Element:
        html = etree.Element(
            "html",
            nsmap={
                None: Namespace.XHTML.value,
                "epub": Namespace.EPUB.value
            }
        )

        head = etree.Element("head")
        html.append(head)

        title = etree.Element("title")
        title.text = title_text
        head.append(title)

        meta = etree.Element(
            "meta",
            attrib={
                "charset": "utf-8"
            }
        )
        head.append(meta)

        for css_file in self.css_files:
            link = etree.Element(
                "link",
                attrib={
                    "href": css_file.as_posix(),
                    "type": "text/css",
                    "rel": "stylesheet"
                }
            )
            head.append(link)

        for js_file in self.js_files:
            script = etree.Element(
                "script",
                attrib={
                    "src": js_file.as_posix(),
                    "type": "text/javascript",
                    "async": "async",
                    "defer": "defer"
                }
            )
            script.text = ""
            head.append(script)

        body = etree.Element("body")
        html.append(body)

        return html
