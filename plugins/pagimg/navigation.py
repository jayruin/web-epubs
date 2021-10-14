from collections.abc import Iterable
from pathlib import Path


def sort_files(files: Iterable[Path]) -> list[Path]:
    try:
        sorted_files = sorted(files, key=lambda file: int(file.stem))
    except ValueError:
        sorted_files = sorted(files, key=lambda file: file.stem)
    return sorted_files


def sort_directories(directories: Iterable[Path]) -> list[tuple[Path, str]]:
    directory_and_text: list[tuple[Path, str]] = []
    try:
        sorted_directories = sorted(
            directories,
            key=lambda path: int(path.stem.split("_")[0])
        )
        for directory in sorted_directories:
            text = "_".join(
                directory.stem.split("_")[1:]
            ).replace("_", " ").title()
            directory_and_text.append((directory, text))
    except ValueError:
        sorted_directories = sorted(directories, key=lambda path: path.stem)
        for directory in sorted_directories:
            text = directory.stem.replace("_", " ").title()
            directory_and_text.append((directory, text))
    return directory_and_text
