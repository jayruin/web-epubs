from __future__ import annotations
from typing import TYPE_CHECKING

from . import epub3, epub2
from ..abcs import EPUB3Document, EPUB2Document
from core.serialize import write_epub3_xhtml_element, write_epub2_xhtml_element
from core.templates import EPUB3Template, EPUB2Template

if TYPE_CHECKING:
    from pathlib import Path


class CoverXHTML(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the cover file.
    """
    def __init__(self, cover_file: Path) -> None:
        self.cover_file = cover_file

    def write_epub3(self, path: Path) -> None:
        template = EPUB3Template([], [])
        html = template.generate_root_element("Cover")

        head = html.find("head")
        assert head is not None
        style = epub3.make_style_element()
        head.append(style)

        body = epub3.make_body_element(self.cover_file)
        html.append(body)

        write_epub3_xhtml_element(html, path)

    def write_epub2(self, path: Path) -> None:
        template = EPUB2Template([])
        html = template.generate_root_element("Cover")

        head = html.find("head")
        assert head is not None
        style = epub2.make_style_element()
        head.append(style)

        body = epub2.make_body_element(self.cover_file)
        html.append(body)

        write_epub2_xhtml_element(html, path)
