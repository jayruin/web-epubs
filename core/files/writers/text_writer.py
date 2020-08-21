from pathlib import Path

from .base_writer import BaseWriter


class TextWriter(BaseWriter):
    def __init__(
        self,
        encoding: str
    ) -> None:
        self.encoding = encoding

    def write(
        self,
        path: Path,
        content: str
    ) -> str:
        with open(path, "w", encoding=self.encoding) as f:
            return f.write(content)
