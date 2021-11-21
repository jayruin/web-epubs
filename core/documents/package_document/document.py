from pathlib import Path
from typing import Optional

from . import epub3, epub2
from ..abcs import EPUB3Document, EPUB2Document
from ..sgml import write_xml_element

from core.project import EPUBMetadata, EPUBResource, TypedAnchor


class EPUB3PackageDocument(EPUB3Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(
        self,
        epub_metadata: EPUBMetadata,
        resources: dict[Path, EPUBResource],
        progression: list[Path],
        pre_paginated: bool
    ) -> None:
        self.epub3_root_element = epub3.make_package_element(
            epub_metadata,
            resources,
            progression,
            pre_paginated,
            epub_metadata.direction,
            self.UNIQUE_IDENTIFIER_ID
        )

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-doc
        """
        write_xml_element(self.epub3_root_element, path)


class EPUB2PackageDocument(EPUB2Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(
        self,
        epub_metadata: EPUBMetadata,
        resources: dict[Path, EPUBResource],
        progression: list[Path],
        toc: Path,
        landmarks: Optional[list[TypedAnchor]] = None
    ) -> None:
        self.epub2_root_element = epub2.make_package_element(
            epub_metadata,
            resources,
            progression,
            toc,
            landmarks,
            self.UNIQUE_IDENTIFIER_ID
        )

    def write_epub2(self, path: Path) -> None:
        """
        http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.0
        """
        write_xml_element(self.epub2_root_element, path)
