from __future__ import annotations
from collections.abc import Collection
from dataclasses import dataclass
from typing import Generic, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

_T_co = TypeVar("_T_co", covariant=True)


@dataclass
class Tree(Generic[_T_co], Collection[_T_co]):
    value: _T_co
    children: list[Tree[_T_co]]

    def __contains__(self, __o: object) -> bool:
        for value in self:
            if value == __o:
                return True
        return False

    def __iter__(self) -> Iterator[_T_co]:
        yield self.value
        for child in self.children:
            yield from child

    def __len__(self) -> int:
        return 1 + sum(len(child) for child in self.children)
