from pathlib import Path

from lxml import etree
from PIL import Image

from .epub3document import EPUB3Document
from core.serialize import write_epub3_xhtml_element
from core.templates import EPUB3Template


class PaginatedImage(EPUB3Document):
    """
    XHTML Fixed-Layout Document containing a single image.
    """
    def __init__(self, image_path: Path, root_path: Path) -> None:
        self.image_path = image_path
        self.width, self.height = Image.open(Path(root_path, image_path)).size

    def epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-contentdocs.html#sec-fxl-icb-html
        """
        template = EPUB3Template([], [])
        html = template.generate_root_element("Paginated Image")

        head = html.find("head")
        assert head is not None
        meta_viewport = make_epub3_meta_viewport_element(
            self.width,
            self.height
        )
        head.append(meta_viewport)

        body = make_epub3_body_element(self.image_path)
        html.append(body)

        write_epub3_xhtml_element(html, path)


def make_epub3_meta_viewport_element(
    width: int,
    height: int
) -> etree._Element:
    meta = etree.Element(
        "meta",
        attrib={
            "name": "viewport",
            "content": f"width={width}, height={height}"
        }
    )
    return meta


def make_epub3_body_element(image_path: Path) -> etree._Element:
    body = etree.Element("body")

    img = etree.Element(
        "img",
        attrib={
            "src": image_path.as_posix()
        }
    )
    body.append(img)

    return body
