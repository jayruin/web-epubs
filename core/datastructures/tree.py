from __future__ import annotations
from collections.abc import Collection
from dataclasses import dataclass
from typing import Generic, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

_T = TypeVar("_T")


@dataclass
class Tree(Generic[_T], Collection[_T]):
    value: _T
    children: list[Tree[_T]]

    def __contains__(self, __o: object) -> bool:
        for value in self:
            if value == __o:
                return True
        return False

    def __iter__(self) -> Iterator[_T]:
        yield self.value
        for child in self.children:
            yield from child

    def __len__(self) -> int:
        return 1 + sum(len(child) for child in self.children)
