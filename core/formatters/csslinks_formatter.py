from pathlib import Path
from typing import Optional

import os.path

from .. import constants
from .base_formatter import BaseFormatter


class CsslinksFormatter(BaseFormatter):
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        assert target is not None
        return "".join(
            [
                f"{constants.INDENT * indents}<"
                "link href=\"{href}\""
                " rel=\"stylesheet\""
                " type=\"text/css\""
                "/>\n".format(
                    href=Path(
                        os.path.relpath(
                            Path(constants.ROOT_PATH_DIR, css_file),
                            Path(constants.ROOT_PATH_DIR, target).parent
                        )
                    ).as_posix()
                )
                for css_file in self.package_contents.css_files
            ]
        ).strip()
