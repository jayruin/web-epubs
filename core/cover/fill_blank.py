from pathlib import Path
import shutil


def fill_blank_cover(
    path: Path
) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        Path("core", "cover", "cover.jpg"),
        path
    )
