from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EPUBCheckResults:
    project: str
    epub_type: str
    fatals: int
    errors: int
    warnings: int

    @classmethod
    def from_text(
        cls,
        project: str,
        epub_type: str,
        text: str
    ) -> EPUBCheckResults:
        lines = text.splitlines()
        messages = lines[-3].replace("Messages: ", "").split(" / ")
        return cls(
            project=project,
            epub_type=epub_type,
            fatals=int(messages[0].split(" ")[0]),
            errors=int(messages[1].split(" ")[0]),
            warnings=int(messages[2].split(" ")[0])
        )
