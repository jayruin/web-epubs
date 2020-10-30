from .copy_parser import CopyParser
from core import constants


class IndentParser(CopyParser):
    def __init__(
        self,
        indents: int
    ) -> None:
        super(IndentParser, self).__init__()

        self.indents: int = indents
        self.should_indent: bool = True

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str]]
    ) -> None:
        if tag == "pre":
            self.should_indent = False
            self.content = self.content.rstrip(" ")
        if tag in constants.HTML_EMPTY_ELEMENTS:
            super(IndentParser, self).handle_startendtag(tag, attrs)
        else:
            super(IndentParser, self).handle_starttag(tag, attrs)

    def handle_endtag(
        self,
        tag: str
    ) -> None:
        if tag == "pre":
            self.should_indent = True
        super(IndentParser, self).handle_endtag(tag)

    def handle_data(
        self,
        data: str
    ) -> None:
        indented_data = data
        if self.should_indent:
            indented_data = indented_data.replace(
                "\n",
                "\n" + constants.INDENT * self.indents
            )
        super(IndentParser, self).handle_data(indented_data)

    def get_content(
        self
    ) -> str:
        self.content = self.content.strip()
        return super(IndentParser, self).get_content()
