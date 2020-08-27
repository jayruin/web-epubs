from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class EPUBCheckResults:
    name: str
    fatals: int
    errors: int
    warnings: int
    infos: int

    @classmethod
    def from_json(
        cls,
        json_file_path: Path
    ) -> EPUBCheckResults:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        checker = data["checker"]
        return cls(
            name=json_file_path.stem.split(".")[0],
            fatals=checker["nFatal"],
            errors=checker["nError"],
            warnings=checker["nWarning"],
            infos=checker["nUsage"]
        )
