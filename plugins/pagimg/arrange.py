from contextlib import ExitStack
import math
from pathlib import Path
import shutil
import tempfile
from typing import Optional


def arrange(directory: Path, suffixes: Optional[list[str]] = None) -> None:
    assert directory.is_dir()
    files: list[Path] = []
    subdirectories: list[Path] = []
    for path in directory.iterdir():
        if path.is_file():
            if suffixes is None or path.suffix in suffixes:
                files.append(path)
        elif path.is_dir():
            subdirectories.append(path)
    try:
        sorted_files = sorted(files, key=lambda file: int(file.stem))
    except ValueError:
        sorted_files = sorted(files, key=lambda file: file.stem)
    if len(sorted_files) > 0:
        digits = math.floor(math.log(len(sorted_files), 10)) + 1
        with ExitStack() as stack:
            temporary_files = [
                stack.enter_context(tempfile.TemporaryFile())
                for _ in range(len(sorted_files))
            ]
            for index, file in enumerate(sorted_files):
                with open(file, "rb") as f:
                    shutil.copyfileobj(f, temporary_files[index])
                temporary_files[index].seek(0)
            pages = [
                file.with_stem(str(index + 1).zfill(digits))
                for index, file in enumerate(sorted_files)
            ]
            for index, page in enumerate(pages):
                with open(page, "wb") as f:
                    shutil.copyfileobj(temporary_files[index], f)
            files_to_delete = set(files) - set(pages)
            for file_to_delete in files_to_delete:
                file_to_delete.unlink()
    for subdirectory in subdirectories:
        arrange(subdirectory, suffixes=suffixes)
