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
        content = ""
        creator_number = 1
        for creator_name in creators:
            content += "".join(
                [
                    f"{constants.INDENT * indents}",
                    f"<dc:creator id=\"creator-id-{creator_number}\">",
                    f"{creator_name}</dc:creator>\n"
                ]
            )
            for creator_role in creators[creator_name]:
                content += "".join(
                    [
                        f"{constants.INDENT * indents}"
                        f"<meta refines=\"#creator-id-{creator_number}\""
                        " property=\"role\" scheme=\"marc:relators\">",
                        f"{creator_role}</meta>\n"
                    ]
                )
            creator_number += 1
        return content.strip()
