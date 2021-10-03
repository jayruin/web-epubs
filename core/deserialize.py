from __future__ import annotations
from collections.abc import Callable
import json
from pathlib import Path
from typing import Any, cast, TypedDict, TypeVar
import yaml

from core.project.anchor import Anchor
from core.project.epub_metadata import EPUBMetadata
from core.project.tree import Tree


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


class NavDict(TypedDict):
    text: str
    href: str
    children: list[NavDict]


def nav_dict_to_tree(data: NavDict) -> Tree[Anchor]:
    return Tree(
        Anchor(data["text"], Path(data["href"])),
        [nav_dict_to_tree(child) for child in data["children"]]
    )


def read_epub_metadata(path: Path) -> EPUBMetadata:
    if path.suffix == ".json":
        load = cast(Any, json).load
    elif path.suffix in [".yaml", ".yml"]:
        load = cast(Any, yaml).load
    else:
        raise ValueError(f"{path.suffix} is unsupported for metadata!")
    with open(path, "rb") as f:
        return EPUBMetadata(**load(f))


def read_nav(path: Path) -> list[Tree[Anchor]]:
    if path.suffix == ".json":
        load = cast(Any, json).load
    elif path.suffix in [".yaml", ".yml"]:
        load = cast(Any, yaml).load
    else:
        raise ValueError(f"{path.suffix} is unsupported for nav!")
    with open(path, "rb") as f:
        return [nav_dict_to_tree(nav_dict) for nav_dict in load(f)]
