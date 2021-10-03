from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

_T = TypeVar("_T")


@dataclass
class Tree(Generic[_T]):
    value: _T
    children: list[Tree[_T]]

    def depth_first_traversal(self) -> Iterable[_T]:
        yield self.value
        for child in self.children:
            yield from child.depth_first_traversal()
