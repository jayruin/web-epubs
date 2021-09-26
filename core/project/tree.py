from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Tree(Generic[T]):
    value: T
    children: list[Tree[T]]

    def depth_first_traversal(self) -> Iterable[T]:
        yield self.value
        for child in self.children:
            yield from child.depth_first_traversal()
