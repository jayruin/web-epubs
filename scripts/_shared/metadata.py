from dataclasses import dataclass
import json
from typing import List

import scripts._shared.constants as constants


@dataclass
class Metadata:
    title: str
    author: str
    languages: List[str]
    date: str = constants.BUILD_TIME

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> None:
        return cls(**json.loads(data))
