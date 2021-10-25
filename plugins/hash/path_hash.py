from collections.abc import Iterable, Mapping
import hmac
from logging import Logger
from pathlib import Path
from typing import cast, Optional, Union

from .multi_hash import MultiHash

PathHash = Union[Mapping[str, str], Mapping[str, "PathHash"]]

CHUNK_SIZE = 2 ** 16


def check_path_hash(
    path: Path,
    expected_path_hash: PathHash,
    logger: Logger
) -> None:
    types = set(type(value) for value in expected_path_hash.values())
    is_terminal = len(types) == 1 and str is types.pop()
    try:
        if is_terminal:
            mismatched_algorithms: list[str] = []
            actual_path_hash = create_path_hash(
                path,
                expected_path_hash.keys()
            )
            for algorithm, expected_hexdigest in expected_path_hash.items():
                expected_hexdigest = cast(str, expected_hexdigest)
                actual_hexdigest = cast(str, actual_path_hash[algorithm])
                if not hmac.compare_digest(
                    expected_hexdigest,
                    actual_hexdigest
                ):
                    mismatched_algorithms.append(algorithm)
            if len(mismatched_algorithms) > 0:
                fails = ",".join(mismatched_algorithms)
                logger.error(f"Path {str(path)}: hashes {fails} do not match")
        else:
            for key, value in expected_path_hash.items():
                child_path = Path(path, key)
                child_expected_path_hash = cast(dict[str, PathHash], value)
                check_path_hash(child_path, child_expected_path_hash, logger)
    except FileNotFoundError:
        logger.error(f"Path {str(path)} not found")


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
    raise FileNotFoundError(f"Path {str(path)} does not exist!")
