from __future__ import annotations
from collections.abc import Iterable, Iterator
from types import TracebackType
from typing import Generic, NoReturn, Optional, TypeVar

_T = TypeVar("_T")


class tqdm(Generic[_T]):
    def __init__(
        self,
        iterable: Iterable[_T] = ...,
        total: int = ...
    ) -> None: ...

    def __enter__(self) -> tqdm[NoReturn]: ...

    def __exit__(
        self, exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> Optional[bool]: ...

    def __iter__(self) -> Iterator[_T]: ...

    def update(self, n: int = ...) -> None: ...
