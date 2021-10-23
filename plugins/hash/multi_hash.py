from collections.abc import Iterable, Mapping, Set
from functools import cache
import hashlib
from typing import Optional


class MultiHash:
    def __init__(self, algorithms: Optional[Iterable[str]] = None) -> None:
        self.hashes: list[hashlib._Hash] = []
        if algorithms is None:
            algorithms = self.default_algorithms
        for algorithm in algorithms:
            try:
                hash = hashlib.new(algorithm)
                self.hashes.append(hash)
            except ValueError:
                continue

    def update(self, data: bytes) -> None:
        for hash in self.hashes:
            hash.update(data)

    def digest(self) -> Mapping[str, bytes]:
        return {hash.name: hash.digest() for hash in self.hashes}

    def hexdigest(self) -> Mapping[str, str]:
        return {hash.name: hash.hexdigest() for hash in self.hashes}

    @classmethod
    @property
    @cache
    def default_algorithms(cls) -> Set[str]:
        algorithms: set[str] = set()
        for algorithm in hashlib.algorithms_guaranteed:
            try:
                hash = hashlib.new(algorithm)
                hash.hexdigest()
                algorithms.add(algorithm)
            except (TypeError, ValueError):
                continue
        return frozenset(algorithms)
