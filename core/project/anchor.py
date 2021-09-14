from dataclasses import dataclass
from typing import Optional


@dataclass
class Anchor:
    text: str
    href: str
    type: Optional[str] = None
