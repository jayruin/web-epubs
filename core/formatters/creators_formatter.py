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
        result = ""
        creator_number = 1
        # for creator_name in creators:
        #     result += "".join(
        #         [
        #             f"{constants.INDENT * indents}",
        #             f"<dc:creator id=\"creator-id-{creator_number}\">",
        #             f"{creator_name}</dc:creator>\n"
        #         ]
        #     )
        #     for creator_role in creators[creator_name]:
        #         result += "".join(
        #             [
        #                 f"{constants.INDENT * indents}"
        #                 f"<meta refines=\"#creator-id-{creator_number}\""
        #                 " property=\"role\" scheme=\"marc:relators\">",
        #                 f"{creator_role}</meta>\n"
        #             ]
        #         )
        #     creator_number += 1

        # The following is a temporary workaround for EPUBCheck reporting:
        # Property "role" cannot be declared more than once to refine
        # a single "creator" or "contributor" property.
        # This is being fixed in https://github.com/w3c/epubcheck/issues/1230
        for creator_name in creators:
            for creator_role in creators[creator_name]:
                result += "".join(
                    [
                        f"{constants.INDENT * indents}",
                        f"<dc:creator id=\"creator-id-{creator_number}\">",
                        f"{creator_name}</dc:creator>\n"
                    ]
                )
                result += "".join(
                    [
                        f"{constants.INDENT * indents}"
                        f"<meta refines=\"#creator-id-{creator_number}\""
                        " property=\"role\" scheme=\"marc:relators\">",
                        f"{creator_role}</meta>\n"
                    ]
                )
                creator_number += 1
        return result.strip()
