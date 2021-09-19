from pathlib import Path

from lxml import etree, html

from .xhtml_template import XHTMLTemplate
from core.constants import Namespace
from core.serialize import write_epub3_xhtml_element


class EPUB3Template(XHTMLTemplate):
    """
    https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-xhtml
    Template for an EPUB3 XHTML content document.
    """
    def __init__(self, css_files: list[Path], js_files: list[Path]) -> None:
        self.css_files = css_files
        self.js_files = js_files

    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        source_html = html.parse(html_file.as_posix())
        title = source_html.find("head/title")
        body = source_html.find("body")
        html_root = self.generate_root_element(title.text)
        html_root.append(body)
        write_epub3_xhtml_element(html_root, xhtml_file, indent=False)

    def generate_root_element(self, title_text: str) -> etree._Element:
        html_root = etree.Element(
            "html",
            nsmap={
                None: Namespace.XHTML.value,
                "epub": Namespace.EPUB.value
            }
        )

        head = etree.Element("head")
        html_root.append(head)

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

        return html_root
