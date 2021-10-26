from pathlib import Path
from typing import Optional

from .navigation import sort_directories
from app.workers.build_jobs import PaginatedImagesBuildJob
from core.datastructures import Tree
from core.project import Anchor


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
    for subdirectory, text in sort_directories(subdirectories):
        tree = subdirectories[subdirectory]
        tree.value.text = text
        children.append(tree)
    sorted_pages = sorted(pages, key=lambda page: int(page.stem))
    if len(sorted_pages) > 0:
        return Tree(Anchor(text, sorted_pages[0]), children)
    elif len(sorted_pages) == 0 and len(children) > 0:
        return Tree(Anchor(text, children[0].value.href), children)
