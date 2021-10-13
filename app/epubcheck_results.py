from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EPUBCheckResults:
    raw: str
    fatals: int
    errors: int
    warnings: int

    @classmethod
    def from_text(cls, text: str) -> EPUBCheckResults:
        lines = text.splitlines()
        messages = lines[-3].replace("Messages: ", "").split(" / ")
        return cls(
            raw=text,
            fatals=int(messages[0].split(" ")[0]),
            errors=int(messages[1].split(" ")[0]),
            warnings=int(messages[2].split(" ")[0])
        )
