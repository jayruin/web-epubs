import json
from pathlib import Path

from app import EPUBCheckResults, Settings
from app.workers import Checker, Installer, Packer
from core.constants import Encoding
from core.runner import subprocess_run


def pack_all(settings: Settings, project_type: str) -> None:
    projects = [
        path.name
        for path in Path(
            settings.expanded_epubs_directory,
            project_type
        ).iterdir()
        if path.is_dir()
    ]
    compression = 0
    packer = Packer(settings)
    packer.pack_projects(projects, project_type, compression)


def check_all(settings: Settings, project_type: str) -> None:
    projects = [
        ".".join(path.stem.split(".")[:-1])
        for path in Path(
            settings.packaged_epubs_directory,
            project_type
        ).iterdir()
        if path.is_file() and path.suffix == ".epub"
    ]
    checker = Checker(settings)
    checker.check_projects(projects, project_type)


def release(settings: Settings, project_type: str) -> None:
    tag = f"release-{project_type}"

    # Delete existing release if it exists
    subprocess_run(["hub", "release", "delete", tag])

    # Create new release
    assets: list[Path] = []
    assets.extend(
        path
        for path in Path(
            settings.packaged_epubs_directory,
            project_type
        ).iterdir()
        if path.is_file() and path.suffix == ".epub"
    )
    assets.extend(
        path
        for path in Path(
            settings.logs_directory,
            project_type
        ).iterdir()
        if path.is_file() and path.suffix == ".txt"
    )
    title = f"GitHub Workflow Release ({project_type})"
    body = f"Automated EPUB ({project_type}) release"
    message = f"{title}\n\n{body}"
    create_args = ["hub", "release", "create"]
    for asset in assets:
        create_args.extend(["-a", asset.as_posix()])
    create_args.extend(["-m", message, tag])
    subprocess_run(create_args)


def summarize(settings: Settings) -> Path:
    project_types = [
        path.name
        for path in settings.logs_directory.iterdir()
        if path.is_dir()
    ]
    summary = {
        "fatals": 0,
        "errors": 0,
        "warnings": 0
    }
    for project_type in project_types:
        for path in Path(settings.logs_directory, project_type).iterdir():
            if path.is_file() and path.suffix == ".txt":
                project = ".".join(path.stem.split(".")[:-1])
                epubcheck_results = EPUBCheckResults.from_text(
                    project,
                    project_type,
                    path.read_text(encoding=Encoding.UTF_8.value)
                )
                summary["fatals"] += epubcheck_results.fatals
                summary["errors"] += epubcheck_results.errors
                summary["warnings"] += epubcheck_results.warnings
    summary_file = Path("epubcheck.summary.json")
    summary_file.write_text(json.dumps(summary), encoding=Encoding.UTF_8.value)
    return summary_file


def release_summary(summary_file: Path) -> None:
    tag = "summary"

    # Delete existing release if it exists
    subprocess_run(["hub", "release", "delete", tag])

    # Create new release
    title = "GitHub Workflow Release EPUBCheck Summary"
    body = "Automated EPUBCheck summary of EPUB releases"
    message = f"{title}\n\n{body}"
    create_args = ["hub", "release", "create"]
    create_args.extend(["-a", summary_file.as_posix()])
    create_args.extend(["-m", message, tag])
    subprocess_run(create_args)


def main() -> None:
    default_settings = Settings()
    installer = Installer(default_settings)
    installer.install_epubcheck()
    project_types = sorted(
        path.name
        for path in default_settings.expanded_epubs_directory.iterdir()
        if path.is_dir()
    )
    for project_type in project_types:
        pack_all(default_settings, project_type)
        check_all(default_settings, project_type)
        release(default_settings, project_type)
    summary_file = summarize(default_settings)
    release_summary(summary_file)


if __name__ == "__main__":
    main()
