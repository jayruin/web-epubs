from __future__ import annotations
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import List

from .. import constants


@dataclass
class Metadata:
    title: str
    author: str
    languages: List[str]
    cover: str = "img/cover.jpg"
    css: List[str] = field(default_factory=list)
    date: str = constants.BUILD_TIME

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> Metadata:
        return cls(**json.loads(data))

    @classmethod
    def from_json_path(
        cls,
        json_path: Path
    ) -> Metadata:
        with open(json_path, "r", encoding="utf-8") as f:
            return cls.from_json(f.read())