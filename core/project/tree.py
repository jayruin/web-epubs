from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Tree(Generic[T]):
    value: T
    children: list[Tree[T]]
