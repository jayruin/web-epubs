from dataclasses import dataclass
from .anchor import Anchor


@dataclass
class TypedAnchor(Anchor):
    type: str
