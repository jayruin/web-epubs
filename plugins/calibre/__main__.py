from argparse import ArgumentParser, Namespace
from pathlib import Path

from . import calibredb
from app import add_project_argparser_args, Settings
from core.project import EPUBProject


def parse_args() -> Namespace:
    module = "plugins.calibre"
    description = "Calibre related integrations"
    parser = ArgumentParser(
        prog=f"python -m {module}",
        description=description
    )
    subparsers = parser.add_subparsers(dest="subparser")
    sync_parser = subparsers.add_parser(
        "sync",
        description="Sync projects with Calibre"
    )
    add_project_argparser_args(sync_parser)
    sync_parser.add_argument("--with-library")
    sync_parser.add_argument("--username")
    sync_parser.add_argument("--password")
    sync_parser.add_argument("--timeout", type=int)
    args = parser.parse_args()
    return args


def sync(args: Namespace) -> None:
    settings = Settings.from_namespace(args)
    new_books: list[str] = []
    for project in args.projects:
        epub_project = EPUBProject(
            Path(
                settings.projects_directory,
                project
            )
        )
        metadata = epub_project.epub_metadata
        search_terms: list[str] = []
        search_terms.append(f"title:\"={metadata.title}\"")
        for creator_name, creator_roles in metadata.creators.items():
            if not creator_roles or "aut" in creator_roles:
                search_terms.append(f"author:\"={creator_name}\"")
        search_expression = " ".join(search_terms)
        book_ids = calibredb.search(
            search_expression,
            with_library=args.with_library,
            username=args.username,
            password=args.password,
            timeout=args.timeout
        )
        ebook_file = Path(
            settings.packaged_epubs_directory,
            args.type,
            f"{project}.{args.type}.epub"
        ).as_posix()
        if not book_ids:
            new_books.append(ebook_file)
        elif len(book_ids) == 1:
            a = calibredb.add_format(
                book_ids[0],
                ebook_file,
                with_library=args.with_library,
                username=args.username,
                password=args.password,
                timeout=args.timeout
            )
            print(a)
        else:
            print(f"Skipping {project} due to ambiguous metadata")
    if new_books:
        calibredb.add(
            new_books,
            with_library=args.with_library,
            username=args.username,
            password=args.password,
            timeout=args.timeout
        )


def main() -> None:
    args = parse_args()
    if args.subparser == "sync":
        sync(args)


main()
