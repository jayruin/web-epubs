import re

title_translation_table = str.maketrans(
    {
        "_": " "
    }
)
title_pattern = re.compile(r"(^|\s)(\S)")


def title_repl(match: re.Match[str]) -> str:
    return f"{match.group(1)}{match.group(2).upper()}"


def make_title(text: str) -> str:
    title = text.translate(title_translation_table)
    title = title_pattern.sub(title_repl, title)
    return title
