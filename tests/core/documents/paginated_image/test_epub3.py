from pathlib import Path

from core.documents import PaginatedImage
from tests.core.documents.shared import check_epub3_document


def test_jpg(paginated_image_jpg: PaginatedImage, expected_file_jpg: Path):
    assert check_epub3_document(paginated_image_jpg, expected_file_jpg)


def test_png(paginated_image_png: PaginatedImage, expected_file_png: Path):
    assert check_epub3_document(paginated_image_png, expected_file_png)
