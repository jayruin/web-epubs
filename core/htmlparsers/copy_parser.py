import html
from html.parser import HTMLParser


class CopyParser(HTMLParser):
    def __init__(
        self
    ) -> None:
        super(CopyParser, self).__init__(convert_charrefs=True)

        self.content: str = ""

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str]]
    ) -> None:
        self.content += f"<{tag}{self._get_attrs_str(attrs)}>"

    def handle_endtag(
        self,
        tag: str
    ) -> None:
        self.content += f"</{tag}>"

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str]]
    ) -> None:
        self.content += f"<{tag}{self._get_attrs_str(attrs)}/>"

    def handle_data(
        self,
        data: str
    ) -> None:
        self.content += html.escape(data, quote=False)

    def get_content(
        self
    ) -> str:
        result = self.content
        self.content = ""
        return result

    def _get_attrs_str(
        self,
        attrs: list[tuple[str, str]]
    ) -> str:
        if attrs:
            attrs_str = " "
        else:
            attrs_str = ""
        attrs_str += " ".join(
            [
                f"{attr[0]}=\"{attr[1]}\""
                for attr in attrs
            ]
        )
        return attrs_str
