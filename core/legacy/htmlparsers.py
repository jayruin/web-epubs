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
        attrs: list[tuple[str, str]]
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
        attrs: list[tuple[str, str]]
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
        attrs: list[tuple[str, str]]
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
        attrs: list[tuple[str, str]]
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
