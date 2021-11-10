from __future__ import annotations
from typing import TYPE_CHECKING

from tests.core.documents.shared import check_epub3_document

if TYPE_CHECKING:
    from pathlib import Path

    from core.documents import PaginatedImage


def test_jpg(paginated_image_jpg: PaginatedImage, expected_file_jpg: Path):
    assert check_epub3_document(paginated_image_jpg, expected_file_jpg)


def test_png(paginated_image_png: PaginatedImage, expected_file_png: Path):
    assert check_epub3_document(paginated_image_png, expected_file_png)
