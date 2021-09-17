from pathlib import Path
from typing import Optional

from core.extendedmimetypes import mimetypes


class EPUBResource:
    def __init__(self, href: Path, mimetype: Optional[str] = None) -> None:
        self.href: Path = href
        self.mimetype: str = (
            mimetype
            or mimetypes.guess_type(href)[0]
            or "application/octet-stream"
        )
        self.id_count: int = 0

    @property
    def manifest_id(self) -> str:
        return f"item-id-{self.id_count}"
