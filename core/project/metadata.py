from pathlib import Path
from typing import Optional, Union
import uuid

from core.constants import BUILD_TIME, UUID_NAMESPACE


class Metadata:
    def __init__(
        self,
        title: str,
        creators: dict[str, list[str]],
        languages: list[str],
        cover: Optional[str] = None,
        css: list[Union[Path, str]] = [],
        js: list[Union[Path, str]] = [],
        date: str = BUILD_TIME,
        identifier: Optional[str] = None
    ) -> None:
        self.title: str = title
        self.creators: dict[str, list[str]] = creators
        self.languages: list[str] = languages
        self.cover: Optional[str] = cover
        self.css: list[Path] = [
            Path(css_file) if isinstance(css_file, str)
            else css_file
            for css_file in css
        ]
        self.js: list[Path] = [
            Path(js_file) if isinstance(js_file, str)
            else js_file
            for js_file in js
        ]
        self.date: str = date
        self.identifier: str = (
            identifier
            or uuid.uuid5(
                uuid.UUID(UUID_NAMESPACE),
                " ".join([title, str(creators), str(languages)])
            ).urn
        )
