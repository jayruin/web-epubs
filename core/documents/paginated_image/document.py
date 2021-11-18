from pathlib import Path

from PIL import Image

from . import epub3
from ..abcs import EPUB3Document
from core.serialize import write_epub3_xhtml_element
from core.templates import EPUB3Template


class PaginatedImage(EPUB3Document):
    """
    XHTML Fixed-Layout Document containing a single image.
    """
    def __init__(self, image_path: Path) -> None:
        self.image_path = image_path
        self.width, self.height = Image.open(image_path).size

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-fxl-icb-html
        """
        template = EPUB3Template([], [])
        html = template.generate_root_element("Paginated Image")

        head = html.find("head")
        assert head is not None
        meta_viewport = epub3.make_meta_viewport_element(
            self.width,
            self.height
        )
        head.append(meta_viewport)

        body = epub3.make_body_element(Path(self.image_path.name))
        html.append(body)

        write_epub3_xhtml_element(html, path)
