from __future__ import annotations
from argparse import Namespace
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class Settings:
    projects_directory: Path = Path("projects")
    expanded_epubs_directory: Path = Path("docs")
    packaged_epubs_directory: Path = Path("dist")
    epubcheck_directory: Path = Path("epubcheck")
    logs_directory: Path = Path("log")
    bundles_directory: Path = Path("bundles")

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> Settings:
        namespace_dict = vars(namespace)
        kwargs = {}
        for field in fields(cls):
            if field.name in namespace_dict:
                if namespace_dict[field.name] is not None:
                    kwargs[field.name] = namespace_dict[field.name]
        return cls(**kwargs)
