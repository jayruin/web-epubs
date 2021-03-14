from pathlib import Path

from core.htmlparsers import IndentParser
from core.packaging import PackageCopier


class ComicbookCopier(PackageCopier):
    def _copy_html(
        self,
        relative_file: str,
        css_links: str
    ) -> None:
        xhtml = relative_file.replace(".html", ".xhtml")
        file_src = Path(self.src_path, relative_file)
        file_dst = Path(self.dst_path, xhtml)
        lines = self.reader.readlines(file_src)
        self.title_parser.feed(lines[1])
        title = self.title_parser.get_content()
        indent_parser = IndentParser(self.template_indents)
        indent_parser.feed("".join(lines[2:]))
        text = indent_parser.get_content()
        self.writer.write(
            file_dst,
            self.template_str.format(
                title=title,
                css=css_links,
                text=text
            )
        )
