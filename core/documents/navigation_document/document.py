from __future__ import annotations
from typing import TYPE_CHECKING

from . import epub3, epub2
from ..abcs import EPUB3Document, EPUB2Document
from core.serialize import write_epub3_xhtml_element, write_epub2_xhtml_element

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
        self.epub3_root_element = epub3.make_html_element(nav_trees, landmarks)
        self.epub2_root_element = epub2.make_html_element(nav_trees)

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-nav
        """
        write_epub3_xhtml_element(self.epub3_root_element, path)

    def write_epub2(self, path: Path) -> None:
        write_epub2_xhtml_element(self.epub2_root_element, path)
