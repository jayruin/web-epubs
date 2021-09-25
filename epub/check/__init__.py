from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil

from core.constants import Encoding, JAVA_EXECUTABLE
from core.runner import subprocess_run
from core.settings import Settings


@dataclass
class EPUBCheckResults:
    project: str
    epub_type: str
    fatals: int
    errors: int
    warnings: int

    @classmethod
    def from_text(
        cls,
        project: str,
        epub_type: str,
        text: str
    ) -> EPUBCheckResults:
        lines = text.splitlines()
        messages = lines[-3].replace("Messages: ", "").split(" / ")
        return cls(
            project=project,
            epub_type=epub_type,
            fatals=int(messages[0].split(" ")[0]),
            errors=int(messages[1].split(" ")[0]),
            warnings=int(messages[2].split(" ")[0])
        )


def check_epub(
    packaged: Path,
    logs: Path,
    epubcheck_jar: Path
) -> EPUBCheckResults:
    results = subprocess_run(
        [
            JAVA_EXECUTABLE,
            "-jar",
            "-Dfile.encoding=UTF-8",
            epubcheck_jar.as_posix(),
            packaged.as_posix()
        ]
    )
    logs.write_text(results, Encoding.UTF_8.value)
    stem_parts = packaged.stem.split(".")
    project = ".".join(stem_parts[:-1])
    epub_type = stem_parts[-1]
    return EPUBCheckResults.from_text(project, epub_type, results)


def check_projects(
    settings: Settings,
    projects: list[str],
    project_type: str
) -> None:
    logs_type_directory = Path(settings.logs_directory, project_type)
    shutil.rmtree(logs_type_directory, ignore_errors=True)
    logs_type_directory.mkdir(parents=True, exist_ok=True)
    epubcheck_jar = Path(settings.epubcheck_directory, "epubcheck.jar")
    fatals = 0
    errors = 0
    warnings = 0
    for project in projects:
        packaged = Path(
            settings.packaged_epubs_directory,
            project_type,
            f"{project}.{project_type}.epub"
        )
        logs = Path(
            logs_type_directory,
            f"{project}.{project_type}.txt"
        )
        epubcheck_results = check_epub(packaged, logs, epubcheck_jar)
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
