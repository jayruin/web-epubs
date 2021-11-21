from abc import ABC, abstractmethod
from pathlib import Path


class XHTMLTemplate(ABC):
    @abstractmethod
    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        pass
