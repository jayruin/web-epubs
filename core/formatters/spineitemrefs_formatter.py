import itertools

from .. import constants
from .base_formatter import BaseFormatter


class SpineitemrefsFormatter(BaseFormatter):
    def run(
        self,
        indents: int
    ) -> str:
        return "".join(
            [
                f"{constants.INDENT * indents}<"
                "itemref idref=\"{idref}\""
                " linear=\"yes\""
                "/>\n".format(
                    idref=self.package_contents.file_id_mapping[href]
                )
                for href in dict.fromkeys(
                    itertools.chain.from_iterable(
                        [
                            nav_node.get_spine_hrefs()
                            for nav_node in self.package_contents.nav_nodes
                        ]
                    )
                )
            ]
        ).strip()