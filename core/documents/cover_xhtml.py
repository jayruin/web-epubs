from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import Namespace
from core.serialize import write_epub2_xhtml_element, write_epub3_xhtml_element
from core.templates import EPUB3Template


class CoverXHTML(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the cover file.
    """
    def __init__(self, cover_file: Path) -> None:
        self.cover_file = cover_file

    def epub3(self, path: Path) -> None:
        template = EPUB3Template([], [])
        html = template.generate_root_element("Cover")

        head = html.find("head")
        assert head is not None
        style = make_style_element()
        head.append(style)

        body = make_epub3_body_element(self.cover_file)
        html.append(body)

        write_epub3_xhtml_element(html, path)

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

        div = etree.Element("div", attrib={"class": "cover-container"})
        body.append(div)

        img = etree.Element(
            "img",
            attrib={
                "alt": "Cover",
                "src": self.cover_file.as_posix()
            }
        )
        div.append(img)

        write_epub2_xhtml_element(html, path)


def make_style_element() -> etree._Element:
    style = etree.Element("style")
    style.text = CSS_STYLE
    return style


def make_epub3_body_element(cover_file: Path) -> etree._Element:
    body = etree.Element("body")

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
            "class": "cover-container"
        }
    )
    section.append(div)

    img = etree.Element(
        "img",
        attrib={
            "alt": "Cover",
            "src": cover_file.as_posix()
        }
    )
    div.append(img)

    return body


CSS_STYLE = """
            .cover-container {
                /* Sizing */
                height: 100%;
                padding: 0px;
                margin: 0px;
                /* Centering */
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .cover-container img {
                max-height: 100%;
                max-width: 100%;
                object-fit: contain;
            }
        """
