from abc import ABC, abstractmethod
from pathlib import Path


class BaseWriter(ABC):
    @abstractmethod
    def write(
        self,
        path: Path,
        content: str
    ) -> None:
        pass

    @abstractmethod
    def append(
        self,
        path: Path,
        content: str
    ) -> None:
        pass
