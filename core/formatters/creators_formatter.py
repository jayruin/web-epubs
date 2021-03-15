from pathlib import Path
from typing import Optional

from .base_formatter import BaseFormatter
from core import constants


class CreatorsFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is None
        creators = self.package_contents.metadata.creators
        return "".join(
            [
                "".join(
                    [
                        f"{constants.INDENT * indents}"
                        f"<dc:creator id=\"creator-id-{creator_number}\">"
                        f"{creator_name}</dc:creator>\n",
                        "" if not creators[creator_name]
                        else f"{constants.INDENT * indents}"
                        f"<meta refines=\"#creator-id-{creator_number}\""
                        " property=\"role\" scheme=\"marc:relators\">"
                        f"{creators[creator_name]}</meta>\n"
                    ]
                )
                for creator_number, creator_name in enumerate(creators)
            ]
        ).strip()
