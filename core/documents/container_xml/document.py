from __future__ import annotations
from typing import TYPE_CHECKING

from . import shared
from ..abcs import EPUB3Document, EPUB2Document
from core.serialize import write_xml_element

if TYPE_CHECKING:
    from pathlib import Path


class ContainerXML(EPUB3Document, EPUB2Document):
    """
    An XML document corresponding to the container.xml file.
    """
    def __init__(self, package_document: Path) -> None:
        root_element = shared.make_container_element(
            package_document
        )
        self.epub3_root_element = root_element
        self.epub2_root_element = root_element

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-ocf.html#sec-container-metainf-container.xml
        """
        write_xml_element(self.epub3_root_element, path)

    def write_epub2(self, path: Path) -> None:
        """
        http://www.idpf.org/doc_library/epub/OCF_2.0.1_draft.doc Section 3.5.1
        """
        write_xml_element(self.epub2_root_element, path)
