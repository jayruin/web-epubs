import os
import subprocess
from typing import Optional


def add(
    files_: list[str],
    portable: str = "",
    help_: Optional[bool] = None,
    with_library_: Optional[str] = None,
    password_: Optional[str] = None,
    username_: Optional[str] = None,
    version_: Optional[bool] = None,
    authors_: Optional[str] = None,
    automerge_: Optional[str] = None,
    cover_: Optional[str] = None,
    duplicates_: Optional[bool] = None,
    empty_: Optional[bool] = None,
    identifiers_: Optional[list[str]] = None,
    isbn_: Optional[str] = None,
    languages_: Optional[str] = None,
    series_: Optional[str] = None,
    series_index_: Optional[str] = None,
    tags_: Optional[str] = None,
    title_: Optional[str] = None,
    add_: Optional[str] = None,
    ignore_: Optional[str] = None,
    one_book_per_directory_: Optional[bool] = None,
    recurse_: Optional[bool] = None
) -> None:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#add
    https://manual.calibre-ebook.com/generated/en/calibredb.html#adding-from-directories
    """
    args = [os.path.join(portable, "calibredb"), "add"]
    if help_:
        args.append("--help")
    if with_library_:
        args.extend(["--with-library", with_library_])
    if password_:
        args.extend(["--password", password_])
    if username_:
        args.extend(["--username", username_])
    if version_:
        args.append("--version")
    if authors_:
        args.extend(["--authors", authors_])
    if automerge_:
        args.extend(["--automerge", automerge_])
    if cover_:
        args.extend(["--cover", cover_])
    if duplicates_:
        args.append("--duplicates")
    if empty_:
        args.append("--empty")
    if identifiers_:
        for identifier_ in identifiers_:
            args.extend(["--identifier", identifier_])
    if isbn_:
        args.extend(["--isbn", isbn_])
    if languages_:
        args.extend(["--languages", languages_])
    if series_:
        args.extend(["--series", series_])
    if series_index_:
        args.extend(["--series-index", series_index_])
    if tags_:
        args.extend(["--tags", tags_])
    if title_:
        args.extend(["--title", title_])
    if add_:
        args.extend(["--add", add_])
    if ignore_:
        args.extend(["--ignore", ignore_])
    if one_book_per_directory_:
        args.append("--one-book-per-directory")
    if recurse_:
        args.append("--recurse")
    args.extend(files_)
    subprocess.run(args, check=True)
