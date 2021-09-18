from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


def depth_first_traversal(tree: Tree[T]) -> Iterable[T]:
    yield tree.value
    for child in tree.children:
        yield from depth_first_traversal(child)


@dataclass
class Tree(Generic[T]):
    value: T
    children: list[Tree[T]]
