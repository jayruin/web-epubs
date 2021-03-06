from pathlib import Path
from typing import Literal

from .navigation import organize_pages
from core.project import SpecialNames
from core.project.epub_project import write_nav

NavFormat = Literal["json", "yaml"]


def autonav(directory: Path, nav_format: NavFormat) -> None:
    special_names = SpecialNames()
    root_tree = organize_pages(directory, root=directory)
    if root_tree is not None:
        nav_trees = root_tree.children
        nav_file = Path(
            directory,
            special_names.nav
        ).with_suffix(f".{nav_format}")
        write_nav(nav_file, nav_trees)
