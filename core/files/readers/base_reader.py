from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    @abstractmethod
    def read(
        path: Path
    ) -> str:
        pass
