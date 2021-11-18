from __future__ import annotations
from typing import TYPE_CHECKING

from . import epub3, epub2
from ..abcs import EPUB3Document, EPUB2Document
from core.serialize import write_epub3_xhtml_element, write_epub2_xhtml_element
from core.templates import EPUB3Template, EPUB2Template

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional

    from core.datastructures import Tree
    from core.project import Anchor, TypedAnchor


class NavigationDocument(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the EPUB Navigation Document.
    May also be used as an inline table of contents.
    """
    def __init__(
        self,
        nav_trees: list[Tree[Anchor]],
        landmarks: Optional[list[TypedAnchor]] = None
    ) -> None:
        self.nav_trees = nav_trees
        self.landmarks = landmarks

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-nav
        """
        template = EPUB3Template([], [])
        html = template.generate_root_element("Navigation")

        head = html.find("head")
        assert head is not None
        style = epub3.make_style_element()
        head.append(style)

        body = epub3.make_body_element(self.nav_trees, self.landmarks)
        html.append(body)

        write_epub3_xhtml_element(html, path)

    def write_epub2(self, path: Path) -> None:
        template = EPUB2Template([])
        html = template.generate_root_element("Navigation")

        head = html.find("head")
        assert head is not None
        style = epub2.make_style_element()
        head.append(style)

        body = epub2.make_body_element(self.nav_trees)
        html.append(body)

        write_epub2_xhtml_element(html, path)
