from pathlib import Path
from typing import Optional

from .base_formatter import BaseFormatter
from core import constants


class Epub2CreatorsFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is None
        creators = self.package_contents.metadata.creators
        result = ""
        for creator_name in creators:
            result += constants.INDENT * indents
            result += "<dc:creator"
            if creators[creator_name]:
                result += " opf:role=\"aut\""
            result += f">{creator_name}</dc:creator>\n"
        return result.strip()
