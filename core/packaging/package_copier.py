from abc import ABC, abstractmethod
import os
from pathlib import Path
import shutil

from core.formatters import CsslinksFormatter
from core.htmlparsers.tag_name_parser import TagNameParser


class PackageCopier(ABC):
    def __init__(
        self,
        src: str,
        dst: str,
        template_str: str,
        template_indents: int,
        csslinks_formatter: CsslinksFormatter
    ) -> None:
        self.src_path: Path = Path(src)
        self.dst_path: Path = Path(dst)
        self.template_str: str = template_str
        self.template_indents: int = template_indents
        self.title_parser: TagNameParser = TagNameParser("title")
        self.h1_parser: TagNameParser = TagNameParser("h1")
        self.csslinks_formatter = csslinks_formatter

        os.makedirs(self.dst_path, exist_ok=True)

    def copy_over(
        self
    ) -> None:
        for dirpath, dirnames, filenames in os.walk(self.src_path):
            for filename in filenames:
                relative_file_path = Path(
                    Path(dirpath).relative_to(self.src_path),
                    filename
                ).as_posix()
                self._copy_file(relative_file_path)

    def _copy_file(
        self,
        relative_file: str
    ) -> None:
        css_links = self.csslinks_formatter.run(
            indents=2,
            target=relative_file
        )
        file_src = Path(self.src_path, relative_file)
        file_dst = Path(self.dst_path, relative_file)
        os.makedirs(file_dst.parents[0], exist_ok=True)
        if file_dst.name.startswith("_"):
            return
        if file_dst.name.endswith(".html"):
            self._copy_html(relative_file, css_links)
        else:
            shutil.copyfile(file_src, file_dst)

    @abstractmethod
    def _copy_html(
        self,
        relative_file: str,
        css_links: str
    ) -> None:
        pass
