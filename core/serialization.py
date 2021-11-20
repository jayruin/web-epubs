from collections.abc import Callable
from functools import partial
import json
from typing import Any, cast, Protocol, TypeVar

import yaml


_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co: ...


class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra) -> Any: ...


def get_dump(suffix: str) -> Callable[[Any, SupportsWrite[str]], None]:
    match suffix:
        case ".json":
            dump = partial(
                cast(Any, json).dump,
                ensure_ascii=False,
                indent=4
            )
        case ".yaml" | ".yml":
            dump = partial(
                cast(Any, yaml).dump,
                allow_unicode=True,
                indent=2,
                sort_keys=False
            )
        case _:
            raise ValueError(f"{suffix} is unsupported!")
    return dump


def get_load(suffix: str) -> Callable[[SupportsRead[bytes]], Any]:
    match suffix:
        case ".json":
            load = cast(Any, json).load
        case ".yaml" | ".yml":
            load = partial(
                cast(Any, yaml).load,
                Loader=yaml.SafeLoader
            )
        case _:
            raise ValueError(f"{suffix} is unsupported!")
    return load
