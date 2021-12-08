from dataclasses import dataclass
from pathlib import Path

from core.project import Anchor


@dataclass
class PaginatedAnchor(Anchor):
    pages: list[Path]
