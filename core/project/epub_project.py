from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from .anchor import Anchor
from .epub_metadata import EPUBMetadata
from .nav_dict import NavDict
from core.constants import Encoding
from core.datastructures import Tree
from core.serialization import get_dump, get_load


class EPUBProject:
    CONTAINER_XML: str = "container.xml"
    COVER_CSS_CLASS: str = "cover-image"
    COVER_XHTML: str = "_cover.xhtml"
    META_INF = "META-INF"
    METADATA: str = "_metadata"
    MIMETYPE_FILE: str = "mimetype"
    NAV: str = "_nav"
    NAVIGATION_DOCUMENT: str = "_nav.xhtml"
    NCX_DOCUMENT: str = "_toc.ncx"
    PACKAGE_DOCUMENT: str = "_package.opf"
    RESOURCES_DIRECTORY: str = "OEBPS"
    SUPPORTED_SUFFIXES: list[str] = [".json", ".yaml", ".yml"]

    def __init__(self, root: Path) -> None:
        self.root: Path = root
        self.name: str = root.stem

        self.epub_metadata: EPUBMetadata = read_any(
            Path(self.root, self.METADATA),
            read_epub_metadata,
            self.SUPPORTED_SUFFIXES
        )

        self.nav_trees: list[Tree[Anchor]] = read_any(
            Path(self.root, self.NAV),
            read_nav,
            self.SUPPORTED_SUFFIXES
        )


_T = TypeVar("_T")


def read_any(
    path: Path,
    read_function: Callable[[Path], _T],
    suffixes: list[str]
) -> _T:
    for suffix in suffixes:
        try:
            return read_function(path.with_suffix(suffix))
        except FileNotFoundError:
            continue
    raise FileNotFoundError


def nav_dict_to_tree(nav_dict: NavDict) -> Tree[Anchor]:
    return Tree(
        Anchor(nav_dict["text"], Path(nav_dict["href"])),
        [nav_dict_to_tree(child) for child in nav_dict["children"]]
    )


def tree_to_nav_dict(tree: Tree[Anchor]) -> NavDict:
    return {
        "text": tree.value.text,
        "href": tree.value.href.as_posix(),
        "children": [tree_to_nav_dict(child) for child in tree.children]
    }


def read_epub_metadata(path: Path) -> EPUBMetadata:
    load = get_load(path.suffix)
    with open(path, "rb") as f:
        return EPUBMetadata(**load(f))


def read_nav(path: Path) -> list[Tree[Anchor]]:
    load = get_load(path.suffix)
    with open(path, "rb") as f:
        return [nav_dict_to_tree(nav_dict) for nav_dict in load(f)]


def write_nav(path: Path, nav: list[Tree[Anchor]]) -> None:
    dump = get_dump(path.suffix)
    with open(path, "w", encoding=Encoding.UTF_8.value) as f:
        dump([tree_to_nav_dict(tree) for tree in nav], f)
