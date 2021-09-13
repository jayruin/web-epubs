from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import (
    DOCTYPE_HTML_EPUB3,
    DOCTYPE_HTML_EPUB2,
    Encoding,
    INDENT,
    Namespace,
    XML_HEADER
)
from core.templates import EPUB3Template


class CoverXHTML(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the cover file.
    """
    def __init__(
        self,
        cover_file: Path,
        css_class: str,
        css_files: list[Path]
    ) -> None:
        self.cover_file = cover_file
        self.css_class = css_class
        self.css_files = css_files

    def epub3(self, path: Path) -> None:
        template = EPUB3Template(self.css_files, [])
        html = template.generate_root_element("Cover")
        body = html.find("body")
        assert body is not None

        section = etree.Element(
            "section",
            attrib={
                etree.QName(Namespace.EPUB.value, "type"): "cover"
            }
        )
        body.append(section)

        div = etree.Element(
            "div",
            attrib={
                "class": self.css_class
            }
        )
        section.append(div)

        img = etree.Element(
            "img",
            attrib={
                "alt": "Cover",
                "src": self.cover_file.as_posix()
            }
        )
        div.append(img)

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
        html = etree.Element("html", nsmap={None: Namespace.XHTML.value})

        head = etree.Element("head")
        html.append(head)

        title = etree.Element("title")
        title.text = "Cover"
        head.append(title)

        meta = etree.Element(
            "meta",
            attrib={
                "http-equiv": "content-type",
                "content": "application/xhtml+xml; charset=utf-8"
            }
        )
        head.append(meta)

        body = etree.Element("body")
        html.append(body)

        div = etree.Element("div", attrib={"class": self.css_class})
        body.append(div)

        img = etree.Element(
            "img",
            attrib={
                "alt": "Cover",
                "src": self.cover_file.as_posix()
            }
        )
        div.append(img)

        etree.indent(html, space=INDENT)
        with open(path, "wb") as f:
            f.write(
                etree.tostring(
                    html,
                    encoding=Encoding.UTF_8.value,
                    doctype="\n".join([XML_HEADER, DOCTYPE_HTML_EPUB2])
                )
            )
