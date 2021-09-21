from __future__ import annotations
import json
from pathlib import Path
from typing import TypedDict

from core.project.anchor import Anchor
from core.project.epub_metadata import EPUBMetadata
from core.project.tree import Tree


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
    with open(path, "rb") as f:
        return EPUBMetadata(**json.load(f))


def read_nav(path: Path) -> list[Tree[Anchor]]:
    with open(path, "rb") as f:
        return [nav_dict_to_tree(nav_dict) for nav_dict in json.load(f)]
