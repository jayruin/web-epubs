from pathlib import Path

from PIL import Image
import pytest

from core.documents import PaginatedImage
from tests.temp import get_temporary_directory


@pytest.fixture
def monochromatic_image() -> Image.Image:
    image = Image.new("RGB", (350, 560), (0, 0, 0))
    return image


@pytest.fixture
def paginated_image_jpg(monochromatic_image: Image.Image) -> PaginatedImage:
    with get_temporary_directory() as directory:
        image_path = Path(directory, "image.jpg")
        monochromatic_image.save(image_path)
        return PaginatedImage(image_path)


@pytest.fixture
def paginated_image_png(monochromatic_image: Image.Image) -> PaginatedImage:
    with get_temporary_directory() as directory:
        image_path = Path(directory, "image.png")
        monochromatic_image.save(image_path)
        return PaginatedImage(image_path)


@pytest.fixture
def expected_file_jpg() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "jpg.xhtml")


@pytest.fixture
def expected_file_png() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "png.xhtml")
