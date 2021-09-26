from pathlib import Path
import shutil
from typing import Any
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from core.runner import make_project_argparser, pool_run
from core.settings import Settings


def add_to_epub(epub_file: ZipFile, entry: Path, expanded: Path) -> None:
    if entry.is_file():
        epub_file.write(entry, entry.relative_to(expanded))
    elif entry.is_dir():
        for child_entry in entry.iterdir():
            add_to_epub(epub_file, child_entry, expanded)


def pack_epub(expanded: Path, packaged: Path, compression: int) -> None:
    mimetype_path = Path(expanded, "mimetype")
    if not mimetype_path.is_file():
        raise FileNotFoundError("Could not find mimetype file!")
    with ZipFile(
        packaged,
        mode="w",
        compression=ZIP_DEFLATED,
        compresslevel=compression
    ) as z:
        z.write(mimetype_path, "mimetype", compress_type=ZIP_STORED)
        for child_path in expanded.iterdir():
            if not (child_path.is_file() and child_path.name == "mimetype"):
                add_to_epub(z, child_path, expanded)


def pack_projects(
    settings: Settings,
    projects: list[str],
    project_type: str,
    compression: int
) -> None:
    packaged_type_directory = Path(
        settings.packaged_epubs_directory,
        project_type
    )
    shutil.rmtree(packaged_type_directory, ignore_errors=True)
    packaged_type_directory.mkdir(parents=True, exist_ok=True)
    args_collection: list[tuple[Path, Path, int]] = []
    kwargs_collection: list[dict[str, Any]] = []
    for project in projects:
        expanded = Path(
            settings.expanded_epubs_directory,
            project_type,
            project
        )
        packaged = Path(
            packaged_type_directory,
            f"{project}.{project_type}.epub"
        )
        args_collection.append((expanded, packaged, compression))
        kwargs_collection.append({})
    for _ in pool_run(
        pack_epub,
        args_collection,
        kwargs_collection,
        "process",
        show_progress=True
    ):
        pass


def main() -> None:
    description = "Pack EPUBs"
    parser = make_project_argparser(description)
    parser.add_argument(
        "-t", "--type",
        default="epub3"
    )
    parser.add_argument(
        "-c", "--compression",
        default=0,
        type=int,
        choices=range(10),
        help="Compression level to use for the output .epub file."
    )
    args = parser.parse_args()
    settings = Settings.from_namespace(args)
    projects: list[str]
    if args.all:
        projects = [
            path.name
            for path in Path(
                settings.expanded_epubs_directory,
                args.type
            ).iterdir()
            if path.is_dir()
        ]
    else:
        projects = args.projects
    pack_projects(settings, projects, args.type, args.compression)


if __name__ == "__main__":
    main()
