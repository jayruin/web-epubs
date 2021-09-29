from pathlib import Path
import shutil
from typing import Any
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from more_itertools import consume

from .app_worker import AppWorker
from core.runner import pool_run


class Packer(AppWorker):
    def pack_projects(
        self,
        projects: list[str],
        project_type: str,
        compression: int
    ) -> None:
        packaged_type_directory = Path(
            self.settings.packaged_epubs_directory,
            project_type
        )
        shutil.rmtree(packaged_type_directory, ignore_errors=True)
        packaged_type_directory.mkdir(parents=True, exist_ok=True)
        args_collection: list[tuple[Path, Path, int]] = []
        kwargs_collection: list[dict[str, Any]] = []
        for project in projects:
            expanded = Path(
                self.settings.expanded_epubs_directory,
                project_type,
                project
            )
            packaged = Path(
                packaged_type_directory,
                f"{project}.{project_type}.epub"
            )
            args_collection.append((expanded, packaged, compression))
            kwargs_collection.append({})
        consume(
            pool_run(
                pack_epub,
                args_collection,
                kwargs_collection,
                "process",
                show_progress=True
            )
        )


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
