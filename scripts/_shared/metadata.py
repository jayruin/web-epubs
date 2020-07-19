from dataclasses import dataclass
import json
from typing import List


@dataclass
class Metadata:
    title: str
    author: str
    languages: List[str]

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> None:
        return cls(**json.loads(data))
