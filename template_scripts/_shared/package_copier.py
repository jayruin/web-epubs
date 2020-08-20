import os
from pathlib import Path
import shutil

from core import constants
from core.htmlparsers.tag_name_parser import TagNameParser


class PackageCopier:
    def __init__(
        self,
        src: str,
        dst: str,
        template_str: str,
        template_indents: int
    ) -> None:
        self.src_path: Path = Path(src)
        self.dst_path: Path = Path(dst)
        self.template_str: str = template_str
        self.template_indents: int = template_indents
        self.title_parser: TagNameParser = TagNameParser("title")
        self.h1_parser: TagNameParser = TagNameParser("h1")

        os.makedirs(self.dst_path, exist_ok=True)

    def copy_over(
        self,
        css_links: str
    ) -> None:
        for dirpath, dirnames, filenames in os.walk(self.src_path):
            for filename in filenames:
                relative_file_path = Path(
                    Path(dirpath).relative_to(self.src_path),
                    filename
                ).as_posix()
                self._copy_file(str(relative_file_path), css_links)

    def _copy_file(
        self,
        relative_file: str,
        css_links: str
    ) -> None:
        file_src = Path(self.src_path, relative_file)
        file_dst = Path(self.dst_path, relative_file)
        os.makedirs(file_dst.parents[0], exist_ok=True)
        if file_dst.name.startswith("_"):
            return
        if file_dst.name.endswith(".html"):
            self._copy_html(relative_file, css_links)
        else:
            shutil.copyfile(file_src, file_dst)

    def _copy_html(
        self,
        relative_file: str,
        css_links: str
    ) -> None:
        xhtml = relative_file.replace(".html", ".xhtml")
        file_src = Path(self.src_path, relative_file)
        file_dst = Path(self.dst_path, xhtml)
        with open(file_src, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.title_parser.feed(lines[1])
        self.h1_parser.feed(lines[2])
        title = self.title_parser.get_content()
        h1 = self.h1_parser.get_content()
        lines = [
            constants.INDENT * self.template_indents + line
            for line in lines[3:]
        ]
        text = "".join(lines).strip()
        with open(file_dst, "w", encoding="utf-8") as f:
            f.write(self.template_str.format(
                title=title,
                css=css_links,
                header=h1,
                text=text
            ))
