from __future__ import annotations
from collections.abc import Iterable
from contextlib import AbstractContextManager
from types import TracebackType
from typing import BinaryIO, Literal, Optional, overload, TypeVar, Union

_T = TypeVar("_T")


class tqdm:

    def __enter__(self) -> tqdm: ...

    def __exit__(
        self, exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> Optional[bool]: ...

    @overload
    def __new__(cls, iterable: Iterable[_T] = ...) -> Iterable[_T]: ...

    @overload
    def __new__(cls, total: int = ...) -> tqdm: ...

    def update(self, n: int = ...) -> None: ...

    @classmethod
    def wrapattr(
        cls,
        stream: BinaryIO,
        method: Union[Literal["read"], Literal["write"]],
        total: Optional[int] = ...
    ) -> AbstractContextManager[BinaryIO]: ...
