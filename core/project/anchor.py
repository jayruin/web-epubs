from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Anchor:
    text: str
    href: Path
    type: Optional[str] = None
