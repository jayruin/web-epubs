from collections.abc import Callable
from pathlib import Path
import shutil

from tqdm import tqdm

from .app_worker import AppWorker
from app.settings import Settings
from app.epubcheck_results import EPUBCheckResults
from core.commands import command
from core.constants import Encoding


class Checker(AppWorker):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        epubcheck_jar = Path(
            self.settings.epubcheck_directory,
            "epubcheck.jar"
        )
        self.epubcheck = make_epubcheck_command(epubcheck_jar)

    def check_projects(self, projects: list[str], project_type: str) -> None:
        logs_type_directory = Path(self.settings.logs_directory, project_type)
        shutil.rmtree(logs_type_directory, ignore_errors=True)
        logs_type_directory.mkdir(parents=True, exist_ok=True)
        fatals = 0
        errors = 0
        warnings = 0
        for project in tqdm(projects):
            packaged = Path(
                self.settings.packaged_epubs_directory,
                project_type,
                f"{project}.{project_type}.epub"
            )
            logs = Path(
                logs_type_directory,
                f"{project}.{project_type}.txt"
            )
            epubcheck_results = self.epubcheck(packaged)
            logs.write_text(epubcheck_results.raw, Encoding.UTF_8.value)
            fatals += epubcheck_results.fatals
            errors += epubcheck_results.errors
            warnings += epubcheck_results.warnings
        print(
            " ".join(
                [
                    "EPUBCheck Results:",
                    str(fatals),
                    "fatals",
                    str(errors),
                    "errors",
                    str(warnings),
                    "warnings"
                ]
            )
        )


def make_epubcheck_command(
    epubcheck_jar: Path
) -> Callable[[Path], EPUBCheckResults]:
    @command(
        ["java", "-jar", "-Dfile.encoding=UTF-8", epubcheck_jar.as_posix()],
        processing=EPUBCheckResults.from_text,
        check_returncode=False
    )
    def epubcheck(packaged: Path, /) -> EPUBCheckResults:
        return EPUBCheckResults("", -1, -1, -1)

    return epubcheck
