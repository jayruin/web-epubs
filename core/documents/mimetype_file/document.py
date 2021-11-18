from __future__ import annotations
from typing import TYPE_CHECKING

from . import shared
from ..abcs import EPUB3Document, EPUB2Document
from core.constants import Encoding

if TYPE_CHECKING:
    from pathlib import Path


class MimetypeFile(EPUB3Document, EPUB2Document):
    """
    The mimetype file in the EPUB Root Directory.
    """
    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-ocf.html#sec-zip-container-mime
        """
        path.write_text(shared.CONTENT, encoding=Encoding.ASCII.value)

    def write_epub2(self, path: Path) -> None:
        """
        http://www.idpf.org/doc_library/epub/OCF_2.0.1_draft.doc Section 4
        """
        path.write_text(shared.CONTENT, encoding=Encoding.ASCII.value)
