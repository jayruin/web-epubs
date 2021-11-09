from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from pathlib import Path


def fill_blank_cover(
    path: Path
) -> None:
    image = Image.new("RGB", (350, 560), (128, 128, 128))
    image.save(path)
