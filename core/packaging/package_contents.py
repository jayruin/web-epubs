import json
import os
from pathlib import Path

from core import constants
from core.config.metadata import Metadata
from core.config.nav_node import NavNode


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
        self.nav_nodes: list[NavNode] = [
            NavNode.from_dict(d)
            for d in json.loads(content)
        ]

        self.files_to_ignore: set[str] = {
            self.metadata.cover
        }

        self.file_id_mapping: dict[str, str] = {}
        self.css_files: list[str] = []
        if self.metadata.css:
            self.css_files = self.metadata.css
        should_search_css = not self.metadata.css
        template_root_path = Path(self.template_dir, constants.ROOT_PATH_DIR)
        src_path = Path(self.src)
        self._traverse_files(src_path)
        if should_search_css:
            self._traverse_css_files(template_root_path)
            self._traverse_css_files(src_path)
            self.css_files = sorted(set(self.css_files))

    def _traverse_files(
        self,
        path: Path
    ) -> None:
        found_files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                relative_path = Path(
                    Path(dirpath).relative_to(path),
                    filename
                )
                relative_file = relative_path.as_posix()
                if relative_path.name.startswith("_"):
                    continue
                if relative_file in self.files_to_ignore:
                    continue
                if relative_file.endswith(".html"):
                    relative_file = relative_file[:-5] + ".xhtml"
                found_files.append(relative_file)
        found_files = sorted(found_files)
        for index, found_file in enumerate(found_files, start=1):
            self.file_id_mapping[found_file] = f"id-{index}"

    def _traverse_css_files(
        self,
        path: Path
    ) -> None:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                relative_path = Path(
                    Path(dirpath).relative_to(path),
                    filename
                )
                relative_file = relative_path.as_posix()
                if relative_file.endswith(".css"):
                    self.css_files.append(relative_file)