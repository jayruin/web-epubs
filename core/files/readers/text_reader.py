from pathlib import Path

from .base_reader import BaseReader


class TextReader(BaseReader):
    def __init__(
        self,
        encoding: str
    ) -> None:
        self.encoding = encoding

    def read(
        self,
        path: Path
    ) -> str:
        with open(path, "r", encoding=self.encoding) as f:
            return f.read()

    def readlines(
        self,
        path: Path
    ) -> list[str]:
        with open(path, "r", encoding=self.encoding) as f:
            return f.readlines()
