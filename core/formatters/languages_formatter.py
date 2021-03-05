from pathlib import Path
from typing import Optional

from .. import constants
from .base_formatter import BaseFormatter


class LanguagesFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is None
        return "".join(
            [
                f"{constants.INDENT * indents}"
                f"<dc:language>{language}</dc:language>\n"
                for language in self.package_contents.metadata.languages
            ]
        ).strip()
