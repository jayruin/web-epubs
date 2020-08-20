from html.parser import HTMLParser
from typing import List, Tuple


class TagNameParser(HTMLParser):
    def __init__(
        self,
        tag_name: str
    ) -> None:
        super(TagNameParser, self).__init__(convert_charrefs=True)

        self.tag_name: str = tag_name
        self.is_active: bool = False
        self.content: str = ""

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
        if tag == self.tag_name:
            self.is_active = True

    def handle_endtag(
        self,
        tag: str
    ) -> None:
        if self.is_active and tag != self.tag_name:
            self.content += f"</{tag}>"
        if tag == self.tag_name:
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
