from collections.abc import Generator
from pathlib import Path
from contextlib import contextmanager, ExitStack
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Optional


@contextmanager
def get_temporary_directory() -> Generator[Path, None, None]:
    stack = ExitStack()
    directory = stack.enter_context(TemporaryDirectory())
    path = Path(directory)
    try:
        yield path
    finally:
        stack.close()


@contextmanager
def get_temporary_file(
    suffix: Optional[str] = None
) -> Generator[Path, None, None]:
    file = NamedTemporaryFile(suffix=suffix, delete=False)
    file.close()
    path = Path(file.name)
    try:
        yield path
    finally:
        path.unlink()
