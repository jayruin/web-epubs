from abc import ABC, abstractmethod
from pathlib import Path


class BaseWriter(ABC):
    @abstractmethod
    def write(
        path: Path,
        content: str
    ) -> None:
        pass
