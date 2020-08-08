import os
from pathlib import Path
import shutil


def create_default_cover(
    path: Path
) -> None:
    os.makedirs(path.parent, exist_ok=True)
    shutil.copyfile(
        "./template_scripts/_shared/cover.jpg",
        path
    )
