from typing import Literal, Optional, Union

from core.commands import command
from core.commands.processing import comma_separated_ints


@command(["calibredb", "add"], flag_repeats={"identifiers"})
def add(
    files: list[str],
    /, *,
    authors: Optional[str] = None,
    automerge: Optional[
        Union[
            Literal["ignore"],
            Literal["overwrite"],
            Literal["new_record"]
        ]
    ] = None,
    cover: Optional[str] = None,
    duplicates: bool = False,
    empty: bool = False,
    identifiers: Optional[list[str]] = None,
    isbn: Optional[str] = None,
    languages: Optional[str] = None,
    series: Optional[str] = None,
    series_index: Optional[int] = None,
    tags: Optional[str] = None,
    title: Optional[str] = None,
    add: Optional[str] = None,
    ignore: Optional[str] = None,
    one_book_per_directory: bool = False,
    recurse: bool = False,

    with_library: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: Optional[int] = None,
) -> str:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#add
    https://manual.calibre-ebook.com/generated/en/calibredb.html#adding-from-directories
    """
    return ""


@command(["calibredb", "add_format"])
def add_format(
    id_: int,
    ebook_file: str,
    /, *,
    dont_replace: bool = False,

    with_library: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: Optional[int] = None,
) -> str:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#add-format
    """
    return ""


@command(["calibredb", "search"], processing=comma_separated_ints)
def search(
    search_expression: str,
    /, *,
    limit: Optional[int] = None,

    with_library: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: Optional[int] = None,
) -> list[int]:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#search
    """
    return []
