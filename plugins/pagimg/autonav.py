from pathlib import Path
from typing import Optional

from app.workers.build_jobs import PaginatedImagesBuildJob
from core.project import Anchor, Tree


def autonav(
    directory: Path,
    root: Path = Path(),
    text: str = ""
) -> Optional[Tree[Anchor]]:
    if not directory.is_dir():
        return None
    pages: list[Path] = []
    subdirectories: dict[Path, Tree[Anchor]] = {}
    children: list[Tree[Anchor]] = []
    for path in directory.iterdir():
        if PaginatedImagesBuildJob.is_page(path):
            pages.append(path.relative_to(root).with_suffix(".xhtml"))
        elif path.is_dir():
            tree = autonav(path, root)
            if tree is not None:
                subdirectories[path] = tree
    try:
        for subdirectory in sorted(
            subdirectories,
            key=lambda path: int(path.stem.split("_")[0])
        ):
            tree = subdirectories[subdirectory]
            tree.value.text = "_".join(
                subdirectory.stem.split("_")[1:]
            ).replace("_", " ")
            children.append(tree)
    except ValueError:
        for subdirectory in sorted(subdirectories, key=lambda path: path.stem):
            tree = subdirectories[subdirectory]
            tree.value.text = subdirectory.stem.replace("_", " ")
            children.append(tree)
    sorted_pages = sorted(pages, key=lambda page: int(page.stem))
    if len(sorted_pages) > 0:
        return Tree(Anchor(text, sorted_pages[0]), children)
    elif len(sorted_pages) == 0 and len(children) > 0:
        return Tree(Anchor(text, children[0].value.href), children)