from abc import ABC, abstractmethod
from pathlib import Path


class EPUB2Document(ABC):
    @abstractmethod
    def epub2(self, path: Path) -> None:
        pass
