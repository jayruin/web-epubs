from __future__ import annotations
from typing import TypeVar


NodeDict = dict[str, "NodeDict"]
NT = TypeVar("NT", bound="Node")


class Node:
    def __init__(
        self,
        value: str,
        children: list[NT]
    ) -> None:
        self.value: str = value
        self.children: list[NT] = children

    @classmethod
    def from_dict(
        cls,
        nd: NodeDict
    ) -> NT:
        value = next(iter(nd))
        return cls(
            value=value,
            children=[
                cls.from_dict(child)
                for child in nd[value]
            ]
        )
