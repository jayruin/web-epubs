from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    @abstractmethod
    def read(
        self,
        path: Path
    ) -> str:
        pass

    @abstractmethod
    def readlines(
        self,
        path: Path
    ) -> list[str]:
        pass
