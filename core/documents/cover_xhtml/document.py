from pathlib import Path

from . import epub3, epub2
from ..abcs import EPUB3Document, EPUB2Document
from ..sgml import write_epub3_xhtml_element, write_epub2_xhtml_element


class CoverXHTML(EPUB3Document, EPUB2Document):
    """
    An XHTML document corresponding to the cover file.
    """
    def __init__(self, cover_file: Path) -> None:
        self.epub3_root_element = epub3.make_html_element(cover_file)
        self.epub2_root_element = epub2.make_html_element(cover_file)

    def write_epub3(self, path: Path) -> None:
        write_epub3_xhtml_element(self.epub3_root_element, path)

    def write_epub2(self, path: Path) -> None:
        write_epub2_xhtml_element(self.epub2_root_element, path)
