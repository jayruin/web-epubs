from dataclasses import dataclass
from pathlib import Path


@dataclass
class Anchor:
    text: str
    href: Path
