from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Literal, Optional, overload, TypeVar

from .anchor import Anchor
from .epub_metadata import EPUBMetadata
from .nav_dict import NavDict
from .page_spread import PageSpread
from .special_names import SpecialNames
from core.constants import Encoding
from core.datastructures import Tree
from core.serialization import get_dump, get_load


class EPUBProject:
    SUPPORTED_SUFFIXES: list[str] = [".json", ".yaml", ".yml"]

    def __init__(
        self,
        root: Path,
        special_names: Optional[SpecialNames] = None
    ) -> None:
        self.root: Path = root
        self.name: str = root.stem
        self.special_names = special_names or SpecialNames()

        self.epub_metadata: EPUBMetadata = read_any(
            Path(self.root, self.special_names.metadata),
            read_epub_metadata,
            self.SUPPORTED_SUFFIXES,
            True
        )

        self.nav_trees: list[Tree[Anchor]] = read_any(
            Path(self.root, self.special_names.nav),
            read_nav,
            self.SUPPORTED_SUFFIXES,
            True
        )

        self.page_spreads: Optional[list[PageSpread]] = read_any(
            Path(self.root, self.special_names.spreads),
            read_spreads,
            self.SUPPORTED_SUFFIXES,
            False
        )


_T = TypeVar("_T")


@overload
def read_any(
    path: Path,
    read_function: Callable[[Path], _T],
    suffixes: list[str],
    required: Literal[True]
) -> _T: ...


@overload
def read_any(
    path: Path,
    read_function: Callable[[Path], _T],
    suffixes: list[str],
    required: Literal[False]
) -> Optional[_T]: ...


def read_any(
    path: Path,
    read_function: Callable[[Path], _T],
    suffixes: list[str],
    required: bool
) -> Optional[_T]:
    for suffix in suffixes:
        try:
            return read_function(path.with_suffix(suffix))
        except FileNotFoundError:
            continue
    if required:
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


def write_nav(path: Path, nav: Iterable[Tree[Anchor]]) -> None:
    dump = get_dump(path.suffix)
    with open(path, "w", encoding=Encoding.UTF_8.value) as f:
        dump([tree_to_nav_dict(tree) for tree in nav], f)


def read_spreads(path: Path) -> list[PageSpread]:
    load = get_load(path.suffix)
    with open(path, "rb") as f:
        return [
            PageSpread(
                Path(page_spread_dict["left"]),
                Path(page_spread_dict["right"])
            )
            for page_spread_dict in load(f)
        ]
