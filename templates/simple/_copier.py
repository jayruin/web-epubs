from pathlib import Path

from core.htmlparsers.indent_parser import IndentParser
from core.packaging import PackageCopier


class SimpleCopier(PackageCopier):
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
        indent_parser = IndentParser(self.template_indents)
        indent_parser.feed("".join(lines[3:]))
        text = indent_parser.get_content()
        with open(file_dst, "w", encoding="utf-8") as f:
            f.write(self.template_str.format(
                title=title,
                css=css_links,
                header=h1,
                text=text
            ))
