from dataclasses import dataclass
from pathlib import Path


@dataclass
class PageSpread:
    left: Path
    right: Path
