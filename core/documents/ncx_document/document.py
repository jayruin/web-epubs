from __future__ import annotations
from typing import TYPE_CHECKING

from . import epub2
from ..abcs import EPUB2Document
from core.serialize import write_xml_element

if TYPE_CHECKING:
    from pathlib import Path

    from core.datastructures import Tree
    from core.project import Anchor


class NCXDocument(EPUB2Document):
    """
    An XML document corresponding to the Navigation Center eXtended.
    """
    def __init__(
        self,
        nav_trees: list[Tree[Anchor]],
        identifier: str,
        title: str
    ) -> None:
        self.epub2_root_element = epub2.make_ncx_element(
            nav_trees,
            identifier,
            title
        )

    def write_epub2(self, path: Path) -> None:
        """
        http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1
        """
        write_xml_element(self.epub2_root_element, path)
