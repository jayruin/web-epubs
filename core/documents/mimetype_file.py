from pathlib import Path

from .epub2document import EPUB2Document
from .epub3document import EPUB3Document
from core.constants import Encoding


class MimetypeFile(EPUB3Document, EPUB2Document):
    """
    The mimetype file in the EPUB Root Directory.
    """
    def epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-ocf.html#sec-zip-container-mime
        """
        path.write_text("application/epub+zip", encoding=Encoding.ASCII.value)

    def epub2(self, path: Path) -> None:
        """
        http://www.idpf.org/doc_library/epub/OCF_2.0.1_draft.doc Section 4
        """
        self.epub3(path)
