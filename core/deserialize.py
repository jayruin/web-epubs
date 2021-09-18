import json
from pathlib import Path

from core.project.epub_metadata import EPUBMetadata


def read_epub_metadata(path: Path) -> EPUBMetadata:
    with open(path, "rb") as f:
        return EPUBMetadata(**json.load(f))
