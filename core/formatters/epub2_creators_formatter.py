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
        creator_number = 1
        for creator_name in creators:
            for creator_role in creators[creator_name]:
                result += "".join(
                    [
                        constants.INDENT * indents,
                        f"<dc:creator id=\"creator-id-{creator_number}\"",
                        f" opf:role=\"{creator_role}\"",
                        f">{creator_name}</dc:creator>\n"
                    ]
                )
                creator_number += 1
        return result.strip()
