import json
from pathlib import Path

from core.project.metadata import Metadata


def read_metadata(path: Path) -> Metadata:
    with open(path, "rb") as f:
        return Metadata(**json.load(f))
