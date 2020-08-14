import itertools
from pathlib import Path
from typing import List

import template_scripts._shared.constants as constants
from template_scripts._shared.id_parser import IdParser
from template_scripts._shared.node import Node
from template_scripts._shared.tag_name_parser import TagNameParser


class NavNode(Node):
    def get_nav_li(
        self,
        indents: int,
        root_dir: str
    ) -> str:
        href = self.value
        content = self.get_content(root_dir)

        li = constants.INDENT * indents
        li += "<li>\n"

        li += constants.INDENT * (indents + 1)
        li += f"<a href=\"{href}\">{content}</a>\n"

        if self.children:
            li += constants.INDENT * (indents + 1)
            li += "<ol>\n"
            li += "".join([
                child.get_nav_li(indents + 2, root_dir)
                for child in self.children
            ])
            li += constants.INDENT * (indents + 1)
            li += "</ol>\n"

        li += constants.INDENT * indents
        li += "</li>\n"

        return li

    def get_content(
        self,
        root_dir: str
    ) -> str:
        href_split = self.value.split("#")
        if len(href_split) == 0:
            return ""
        if len(href_split) == 1:
            parser = TagNameParser("title")
        else:
            parser = IdParser(href_split[1])
        href = href_split[0].replace("xhtml", "html", 1)
        try:
            with open(Path(root_dir, href), "r", encoding="utf-8") as f:
                parser.feed(f.read())
        except FileNotFoundError:
            return ""
        return parser.get_content()

    def get_spine_hrefs(
        self
    ) -> List[str]:
        hrefs = [self.value.split("#")[0]]
        hrefs.extend(itertools.chain.from_iterable([
            child.get_spine_hrefs()
            for child in self.children
        ]))
        return hrefs
