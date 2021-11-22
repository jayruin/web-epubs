from __future__ import annotations
from argparse import Namespace
from collections.abc import Mapping
from dataclasses import dataclass, fields
import os
from pathlib import Path
from typing import Any, get_type_hints


@dataclass
class Settings:
    projects_directory: Path = Path("projects")
    expanded_epubs_directory: Path = Path("docs")
    packaged_epubs_directory: Path = Path("dist")
    epubcheck_directory: Path = Path("epubcheck")
    logs_directory: Path = Path("log")
    bundles_directory: Path = Path("bundles")

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> Settings:
        normalized_mapping = {
            key.lower(): value
            for key, value in mapping.items()
        }
        kwargs = {}
        resolved_types = get_type_hints(cls)
        for field in fields(cls):
            field_type = resolved_types[field.name]
            normalized_field_name = field.name.lower()
            if normalized_field_name in normalized_mapping:
                value = normalized_mapping[normalized_field_name]
                if value is None:
                    continue
                elif not isinstance(value, field_type):
                    value = field_type(value)
                kwargs[field.name] = value
        return cls(**kwargs)

    @classmethod
    def from_env(cls) -> Settings:
        return cls.from_mapping(os.environ)

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> Settings:
        return cls.from_mapping(vars(namespace))
