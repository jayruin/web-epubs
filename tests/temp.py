from __future__ import annotations
from pathlib import Path
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Optional


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
