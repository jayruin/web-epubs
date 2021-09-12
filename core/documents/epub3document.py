from abc import ABC, abstractmethod
from pathlib import Path


class EPUB3Document(ABC):
    @abstractmethod
    def epub3(self, path: Path) -> None:
        pass
