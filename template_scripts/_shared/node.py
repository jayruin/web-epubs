from __future__ import annotations
from typing import Dict, List, TypeVar


NodeDict = Dict[str, "NodeDict"]
NT = TypeVar("NT", bound="Node")


class Node:
    def __init__(
        self,
        value: str,
        children: List[NT]
    ) -> None:
        self.value: str = value
        self.children: List[NT] = children

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
