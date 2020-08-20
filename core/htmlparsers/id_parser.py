from html.parser import HTMLParser
from typing import List, Tuple


class IdParser(HTMLParser):
    def __init__(
        self,
        id_value: str
    ) -> None:
        super(IdParser, self).__init__(convert_charrefs=True)

        self.id_value: str = id_value
        self.is_active: bool = False
        self.content: str = ""
        self.tag: str = ""

    def handle_starttag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        if self.is_active:
            tag_items = [tag]
            for attr, val in attrs:
                tag_items.append(f"{attr}=\"{val}\"")
            self.content += "<{0}>".format(" ".join(tag_items))
        if ("id", self.id_value) in attrs:
            self.is_active = True
            self.tag = tag

    def handle_endtag(
        self,
        tag: str
    ) -> None:
        if self.is_active and tag != self.tag:
            self.content += f"</{tag}>"
        if tag == self.tag:
            self.is_active = False

    def handle_startendtag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        if self.is_active:
            tag_items = [tag]
            for attr, val in attrs:
                tag_items.append(f"{attr}=\"{val}\"")
            self.content += "<{0}/>".format(" ".join(tag_items))

    def handle_data(
        self,
        data: str
    ) -> None:
        if self.is_active:
            self.content += data

    def get_content(
        self
    ) -> str:
        result = self.content
        self.content = ""
        return result
