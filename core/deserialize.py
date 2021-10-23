from collections.abc import Callable
import json
from pathlib import Path
from typing import Any, cast, TypeVar

import yaml

from core.project.anchor import Anchor
from core.project.epub_metadata import EPUBMetadata
from core.project.nav_dict import NavDict
from core.project.tree import Tree


_T = TypeVar("_T")


def get_load(suffix: str) -> Any:
    match suffix:
        case ".json":
            load = cast(Any, json).load
        case ".yaml" | ".yml":
            load = cast(Any, yaml).load
        case _:
            raise ValueError(f"{suffix} is unsupported!")
    return load


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


def read_epub_metadata(path: Path) -> EPUBMetadata:
    load = get_load(path.suffix)
    with open(path, "rb") as f:
        return EPUBMetadata(**load(f))


def read_nav(path: Path) -> list[Tree[Anchor]]:
    load = get_load(path.suffix)
    with open(path, "rb") as f:
        return [nav_dict_to_tree(nav_dict) for nav_dict in load(f)]
