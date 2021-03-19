from pathlib import Path
from typing import Optional

from .base_formatter import BaseFormatter


class NavpointsFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is None
        return "".join(
            [
                nav_node.get_ncx_navpoint(
                    indents=indents,
                    root_dir=self.package_contents.src,
                    navpoint_id=f"ncx-{count}"
                )
                for count, nav_node in enumerate(
                    self.package_contents.nav_nodes,
                    start=1
                )
            ]
        ).strip()
