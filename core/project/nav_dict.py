from __future__ import annotations
from typing import TypedDict


class NavDict(TypedDict):
    text: str
    href: str
    children: list[NavDict]
