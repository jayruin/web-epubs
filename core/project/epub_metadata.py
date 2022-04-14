from pathlib import Path
from typing import Optional, Union
import uuid

from core.constants import BUILD_TIME, UUID_NAMESPACE


class EPUBMetadata:
    def __init__(
        self,
        title: str,
        creators: Optional[dict[str, list[str]]] = None,
        languages: Optional[list[str]] = None,
        cover: Optional[Union[Path, str]] = None,
        direction: Optional[str] = None,
        css: Optional[list[Union[Path, str]]] = None,
        js: Optional[list[Union[Path, str]]] = None,
        date: Optional[str] = None,
        identifier: Optional[str] = None,
        modified: str = BUILD_TIME
    ) -> None:
        self.title: str = title
        self.creators: dict[str, list[str]] = creators or {}
        self.languages: list[str] = languages or ["en"]
        self.cover: Optional[Path] = (
            Path(cover) if isinstance(cover, str)
            else cover
        )
        self.direction: Optional[str] = direction
        self.css: list[Path] = [
            Path(css_file) if isinstance(css_file, str)
            else css_file
            for css_file in (css or [])
        ]
        self.js: list[Path] = [
            Path(js_file) if isinstance(js_file, str)
            else js_file
            for js_file in (js or [])
        ]
        self.date: Optional[str] = date
        self.identifier: str = (
            identifier
            or uuid.uuid5(
                uuid.UUID(UUID_NAMESPACE),
                " ".join([title, str(creators), str(languages)])
            ).urn
        )
        self.modified: str = modified
