from pathlib import Path

from PIL import Image

from . import epub3
from ..abcs import EPUB3Document
from core.serialize import write_epub3_xhtml_element


class PaginatedImage(EPUB3Document):
    """
    XHTML Fixed-Layout Document containing a single image.
    """
    def __init__(self, image_path: Path) -> None:
        image_path = image_path
        width, height = Image.open(image_path).size
        src = Path(image_path.name)
        self.epub3_root_element = epub3.make_html_element(width, height, src)

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-fxl-icb-html
        """
        write_epub3_xhtml_element(self.epub3_root_element, path)
