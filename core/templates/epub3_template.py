from collections.abc import Iterable
import os.path
from pathlib import Path
from typing import Optional

from lxml import etree, html

from .xhtml_template import XHTMLTemplate
from core.constants import Namespace
from core.serialize import write_epub3_xhtml_element


class EPUB3Template(XHTMLTemplate):
    """
    https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-xhtml
    Template for an EPUB3 XHTML content document.
    """
    def __init__(
        self,
        css_files: list[Path],
        js_files: list[Path],
        base: Optional[Path] = None
    ) -> None:
        self.css_files = css_files
        self.js_files = js_files
        self.base = base

    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        source_html = html.parse(html_file.as_posix())
        title = source_html.find("head/title")
        body = source_html.find("body")
        html_root = self.generate_root_element(title.text, xhtml_file)
        html_root.append(body)
        write_epub3_xhtml_element(html_root, xhtml_file, indent=False)

    def relative_to(
        self,
        paths: list[Path],
        xhtml_file: Optional[Path] = None
    ) -> Iterable[Path]:
        for path in paths:
            if self.base and xhtml_file:
                yield Path(
                    os.path.relpath(
                        path,
                        xhtml_file.parent.relative_to(self.base)
                    )
                )
            else:
                yield path

    def generate_root_element(
        self,
        title_text: str,
        xhtml_file: Optional[Path] = None
    ) -> etree._Element:
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

        for css_file in self.relative_to(self.css_files, xhtml_file):
            link = etree.Element(
                "link",
                attrib={
                    "href": css_file.as_posix(),
                    "type": "text/css",
                    "rel": "stylesheet"
                }
            )
            head.append(link)

        for js_file in self.relative_to(self.js_files, xhtml_file):
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
