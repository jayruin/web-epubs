from collections.abc import Iterable
from pathlib import Path
import re
from typing import Optional

from .paginated_anchor import PaginatedAnchor
from app.workers.build_jobs import PaginatedImagesBuildJob
from core.datastructures import Tree


def sort_files(files: Iterable[Path]) -> list[Path]:
    try:
        sorted_files = sorted(files, key=lambda file: int(file.stem))
    except ValueError:
        sorted_files = sorted(files, key=lambda file: file.stem)
    return sorted_files


def sort_directories(directories: Iterable[Path]) -> list[tuple[Path, str]]:
    directory_and_text: list[tuple[Path, str]] = []
    try:
        sorted_directories = sorted(
            directories,
            key=lambda path: int(path.stem.split("_")[0])
        )
        for directory in sorted_directories:
            text = make_title("_".join(directory.stem.split("_")[1:]))
            directory_and_text.append((directory, text))
    except ValueError:
        sorted_directories = sorted(directories, key=lambda path: path.stem)
        for directory in sorted_directories:
            text = make_title(directory.stem)
            directory_and_text.append((directory, text))
    return directory_and_text


def organize_pages(
    directory: Path,
    root: Path = Path(),
    text: str = ""
) -> Optional[Tree[PaginatedAnchor]]:
    if not directory.is_dir():
        return None
    pages: list[Path] = []
    subdirectories: list[Path] = []
    children: list[Tree[PaginatedAnchor]] = []
    for path in directory.iterdir():
        if PaginatedImagesBuildJob.is_page(path):
            pages.append(path)
        elif path.is_dir():
            subdirectories.append(path)
    for subdirectory, subdirectory_text in sort_directories(subdirectories):
        tree = organize_pages(subdirectory, root, subdirectory_text)
        if tree is not None:
            children.append(tree)
    sorted_pages = sort_files(pages)
    if len(sorted_pages) > 0:
        href = sorted_pages[0].relative_to(root).with_suffix(".xhtml")
    elif len(sorted_pages) == 0 and len(children) > 0:
        href = children[0].value.href
    else:
        return None
    return Tree(PaginatedAnchor(text, href, sorted_pages), children)


_title_pattern = re.compile(r"(^|\s)(\S)")


def _title_repl(match: re.Match[str]) -> str:
    return f"{match.group(1)}{match.group(2).upper()}"


def make_title(text: str) -> str:
    title = text.replace("_", " ")
    title = _title_pattern.sub(_title_repl, title)
    return title
