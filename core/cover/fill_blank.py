import os
from pathlib import Path
import shutil


def fill_blank_cover(
    path: Path
) -> None:
    if path.exists():
        return
    os.makedirs(path.parent, exist_ok=True)
    shutil.copyfile(
        "./core/cover/cover.jpg",
        path
    )
