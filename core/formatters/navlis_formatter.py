from pathlib import Path
from typing import Optional

from .base_formatter import BaseFormatter


class NavlisFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is None
        return "".join(
            [
                nav_node.get_nav_li(
                    indents=indents,
                    root_dir=self.package_contents.src
                )
                for nav_node in self.package_contents.nav_nodes
            ]
        ).strip()
