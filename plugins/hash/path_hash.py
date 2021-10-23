from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Optional, Union

from .multi_hash import MultiHash

PathHash = Union[Mapping[str, str], Mapping[str, "PathHash"]]

CHUNK_SIZE = 2 ** 16


def create_path_hash(
    path: Path,
    algorithms: Optional[Iterable[str]] = None
) -> PathHash:
    if path.is_file():
        multi_hash = MultiHash(algorithms)
        with open(path, "rb") as f:
            while data := f.read(CHUNK_SIZE):
                multi_hash.update(data)
        return multi_hash.hexdigest()
    elif path.is_dir():
        return {
            child_path.name: create_path_hash(child_path, algorithms)
            for child_path in path.iterdir()
        }
    return {}
