from pathlib import Path
from typing import Type

from core.files.readers.text_reader import TextReader
from core.files.writers.text_writer import TextWriter
from core.formatters import CsslinksFormatter
from core.htmlparsers import IndentParser, TagNameParser
from core.packaging import PackageCopier


class SimpleCopier(PackageCopier):
    def __init__(
        self,
        src: str,
        dst: str,
        template_str: str,
        template_indents: int,
        csslinks_formatter: CsslinksFormatter,
        reader: Type[TextReader],
        writer: Type[TextWriter]
    ) -> None:
        super(SimpleCopier, self).__init__(
            src,
            dst,
            template_str,
            template_indents,
            csslinks_formatter,
            reader,
            writer
        )
        self.h1_parser: TagNameParser = TagNameParser("h1")

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
        self.h1_parser.feed(lines[2])
        title = self.title_parser.get_content()
        h1 = self.h1_parser.get_content()
        indent_parser = IndentParser(self.template_indents)
        indent_parser.feed("".join(lines[3:]))
        text = indent_parser.get_content()
        self.writer.write(
            file_dst,
            self.template_str.format(
                title=title,
                css=css_links,
                header=h1,
                text=text
            )
        )
