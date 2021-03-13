import json
import math
import os
from pathlib import Path
import shutil
import zipfile

from core import constants
from core.files.readers import Utf8Reader
from core.files.writers import Utf8Writer


class ComicbookProject:
    def __init__(
        self,
        project_name: str
    ) -> None:
        self.project_directory: Path = Path(
            constants.HTML_DIRECTORY,
            project_name
        )
        self.nav_file: Path = Path(self.project_directory, constants.NAV_JSON)
        self.reader = Utf8Reader()
        self.writer = Utf8Writer()

    def create_volume(
        self,
        volume_name: str,
        cover_chapter_name: str
    ) -> None:
        volume_html = f"{cover_chapter_name}.html"
        volume_xhtml = Path(
            volume_name,
            f"{cover_chapter_name}.xhtml"
        ).as_posix()
        content = "\n".join(
            [
                "<!DOCTYPE html>",
                f"<title>{volume_name}</title>",
                "",
                ""
            ]
        )
        volume_directory = Path(self.project_directory, volume_name)
        volume_directory.mkdir()
        self.writer.write(
            Path(
                volume_directory,
                volume_html
            ),
            content
        )
        nav = json.loads(self.reader.read(self.nav_file))
        nav.append({volume_xhtml: []})
        self.writer.write(self.nav_file, json.dumps(nav, indent=4))

    def import_chapter(
        self,
        volume_name: str,
        chapter: Path
    ) -> None:
        if chapter.is_dir():
            pages = self._copy_pages_from_directory(volume_name, chapter)
            chapter_exists = self._write_chapter_html(
                volume_name,
                chapter.name,
                pages
            )
            if not chapter_exists:
                self._add_chapter_to_nav(volume_name, chapter.name)
        elif chapter.suffix == ".cbz":
            pages = self._copy_pages_from_cbz(volume_name, chapter)
            chapter_exists = self._write_chapter_html(
                volume_name,
                chapter.stem,
                pages
            )
            if not chapter_exists:
                self._add_chapter_to_nav(volume_name, chapter.stem)
        else:
            raise ValueError("Invalid chapter to import from!")

    def _copy_pages_from_directory(
        self,
        volume_name: str,
        chapter: Path
    ) -> list[str]:
        copied_pages = []
        new_chapter = Path(self.project_directory, volume_name, chapter.name)
        new_chapter.mkdir()
        digits = self._get_digits_needed(
            len(
                [
                    entry
                    for entry in chapter.iterdir()
                    if entry.is_file()
                ]
            )
        )
        page_number = 1
        with os.scandir(chapter) as it:
            for entry in sorted(it, key=lambda e: e.name):
                if entry.is_file():
                    new_page = Path(
                        new_chapter,
                        "".join(
                            [
                                f"{str(page_number).zfill(digits)}",
                                f"{Path(entry.path).suffix}"
                            ]
                        )
                    )
                    shutil.copyfile(entry.path, new_page)
                    copied_pages.append(new_page.name)
                    page_number += 1
        return copied_pages

    def _copy_pages_from_cbz(
        self,
        volume_name: str,
        chapter: Path
    ) -> list[str]:
        copied_pages = []
        new_chapter = Path(self.project_directory, volume_name, chapter.stem)
        new_chapter.mkdir()
        with zipfile.ZipFile(chapter, "r") as z:
            root_zipfile_path = zipfile.Path(z)
            pages = sorted(
                child.name
                for child in root_zipfile_path.iterdir()
                if child.is_file()
            )
            digits = self._get_digits_needed(len(pages))
            page_number = 1
            for page in pages:
                new_page_name = "".join(
                    [
                        f"{str(page_number).zfill(digits)}",
                        f"{Path(page).suffix}"
                    ]
                )
                page_zip_info = z.getinfo(page)
                page_zip_info.filename = new_page_name
                z.extract(page_zip_info, new_chapter)
                copied_pages.append(new_page_name)
                page_number += 1
        return copied_pages

    def _write_chapter_html(
        self,
        volume_name,
        chapter_name,
        pages: list[str]
    ) -> bool:
        chapter_html = f"{chapter_name}.html"
        chapter_html_path = Path(
            self.project_directory,
            volume_name,
            chapter_html
        )
        chapter_exists = chapter_html_path.exists()
        if not chapter_exists:
            self.writer.write(
                chapter_html_path,
                "\n".join(
                    [
                        "<!DOCTYPE html>",
                        f"<title>{chapter_name}</title>",
                        "",
                        ""
                    ]
                )
            )
        content = "\n".join(
            [
                "\n".join(
                    [
                        "<div class=\"cb-page\">",
                        "".join(
                            [
                                constants.INDENT,
                                "<img src=\"",
                                Path(chapter_name, page).as_posix(),
                                "\" />"
                            ]
                        ),
                        "</div>"
                    ]
                )
                for page in pages
            ]
        )
        self.writer.append(chapter_html_path, content)
        return chapter_exists

    def _add_chapter_to_nav(
        self,
        volume_name: str,
        chapter_name: str
    ) -> None:
        chapter_xhtml = Path(
            volume_name,
            f"{chapter_name}.xhtml"
        ).as_posix()
        nav = json.loads(self.reader.read(self.nav_file))
        for nav_dict in nav:
            for key in nav_dict.keys():
                if key.split("/")[0] == volume_name:
                    nav_dict[key].append({chapter_xhtml: []})
                    self.writer.write(self.nav_file, json.dumps(nav, indent=4))
                    return nav

    @staticmethod
    def _get_digits_needed(
        number_of_files: int
    ) -> int:
        return math.floor(math.log(number_of_files, 10)) + 1
