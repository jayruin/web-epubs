from collections.abc import Iterable
import os.path
from pathlib import Path
from typing import Optional

from lxml import etree, html

from .xhtml_template import XHTMLTemplate
from core.constants import Encoding, Namespace
from core.documents.sgml import write_epub2_xhtml_element


class EPUB2Template(XHTMLTemplate):
    """
    http://idpf.org/epub/20/spec/OPS_2.0.1_draft.htm#Section1.4.1.2
    Template for an EPUB2 XHTML content document.
    """
    def __init__(
        self,
        css_files: list[Path],
        base: Optional[Path] = None
    ) -> None:
        self.css_files = css_files
        self.base = base

    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        parser = html.HTMLParser(encoding=Encoding.UTF_8.value)
        with open(html_file, encoding=Encoding.UTF_8.value) as f:
            source_html = html.document_fromstring(
                f.read(),
                parser=parser,
                ensure_head_body=True
            )
        title = source_html.head.find("title")
        body = source_html.body
        html_root = self.generate_root_element(title.text, xhtml_file)
        html_root.append(body)
        write_epub2_xhtml_element(html_root, xhtml_file, indent=False)

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
                None: Namespace.XHTML.value
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
                "http-equiv": "content-type",
                "content": "application/xhtml+xml; charset=utf-8"
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

        return html_root
