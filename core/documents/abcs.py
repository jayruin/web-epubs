from abc import ABC, abstractmethod
from pathlib import Path


class EPUB3Document(ABC):
    @abstractmethod
    def write_epub3(self, path: Path) -> None:
        pass


class EPUB2Document(ABC):
    @abstractmethod
    def write_epub2(self, path: Path) -> None:
        pass
