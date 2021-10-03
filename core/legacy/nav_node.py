from __future__ import annotations
import itertools
from pathlib import Path
from typing import Any

from core import constants
from .htmlparsers import IdParser, TagNameParser


class NavNode:
    def __init__(
        self,
        value: str,
        children: list[NavNode]
    ) -> None:
        self.value: str = value
        self.children: list[NavNode] = children

    @classmethod
    def from_dict(
        cls,
        nd: Any
    ) -> NavNode:
        value = next(iter(nd))
        return cls(
            value=value,
            children=[
                cls.from_dict(child)
                for child in nd[value]
            ]
        )

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
    ) -> list[str]:
        hrefs = [self.value.split("#")[0]]
        hrefs.extend(itertools.chain.from_iterable([
            child.get_spine_hrefs()
            for child in self.children
        ]))
        return hrefs

    def get_ncx_navpoint(
        self,
        indents: int,
        root_dir: str,
        navpoint_id: str
    ) -> str:
        href = self.value
        content = self.get_content(root_dir)

        navpoint = constants.INDENT * indents
        navpoint += f"<navPoint id=\"{navpoint_id}\">\n"

        navpoint += constants.INDENT * (indents + 1)
        navpoint += "<navLabel>\n"
        navpoint += constants.INDENT * (indents + 2)
        navpoint += f"<text>{content}</text>\n"
        navpoint += constants.INDENT * (indents + 1)
        navpoint += "</navLabel>\n"

        navpoint += constants.INDENT * (indents + 1)
        navpoint += f"<content src=\"{href}\"/>\n"

        if self.children:
            navpoint += "".join([
                child.get_ncx_navpoint(
                    indents + 1,
                    root_dir,
                    navpoint_id + f"-{count}"
                )
                for count, child in enumerate(self.children, start=1)
            ])

        navpoint += constants.INDENT * indents
        navpoint += "</navPoint>\n"

        return navpoint
