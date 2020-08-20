import json
import os
from pathlib import Path
from typing import Dict, List

from core import constants
from .config.metadata import Metadata
from .config.nav_node import NavNode


class PackageContents:
    def __init__(
        self,
        src: str,
        template_dir: str
    ) -> None:
        self.src: str = src
        self.template_dir: str = template_dir

        self.metadata: Metadata = Metadata.from_json_path(
            Path(
                self.src,
                constants.METADATA_JSON
            )
        )

        with open(Path(
            self.src,
            constants.NAV_JSON
        ), "r", encoding="utf-8") as f:
            content = f.read()
        self.nav_nodes: List[NavNode] = [
            NavNode.from_dict(d)
            for d in json.loads(content)
        ]

        self.file_id_mapping: Dict[str, str] = {}
        self.css_files: List[str] = []
        if self.metadata.css:
            self.css_files = self.metadata.css
        should_search_css = not self.metadata.css
        self._traverse_files(
            Path(self.template_dir),
            should_search_css
        )
        self._traverse_files(
            Path(self.src),
            should_search_css
        )
        if should_search_css:
            self.css_files = sorted(set(self.css_files))

    def _traverse_files(
        self,
        path: Path,
        should_search_css: bool
    ) -> None:
        next_index = 1
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                relative_file = Path(
                    Path(dirpath).relative_to(path),
                    filename
                ).as_posix()
                if relative_file.startswith("_"):
                    return
                if should_search_css and relative_file.endswith(".css"):
                    self.css_files.append(relative_file)
                if relative_file.endswith(".html"):
                    relative_file = relative_file[:-5] + ".xhtml"
                self.file_id_mapping[relative_file] = f"id-{next_index}"
                next_index += 1
