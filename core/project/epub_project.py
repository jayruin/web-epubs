import json
from pathlib import Path

from .anchor import Anchor
from .epub_metadata import EPUBMetadata
from .tree import Tree
from core.config import NavNode
from core.deserialize import read_epub_metadata
from core.legacy import navnode_to_tree


class EPUBProject:
    COVER_CSS_CLASS: str = "cover-image"
    HTML_DIRECTORY: str = "html"
    METADATA_JSON: str = "_metadata.json"
    NAV_JSON: str = "_nav.json"
    PACKAGE_OPF: str = "_package.opf"
    RESOURCES_DIRECTORY: str = "OEBPS"
    UNZIPPED_EPUBS_DIRECTORY: str = "docs"

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.source: Path = Path(self.HTML_DIRECTORY, name)

        self.epub_metadata: EPUBMetadata = read_epub_metadata(
            Path(self.source, self.METADATA_JSON)
        )

        self.nav_trees: list[Tree[Anchor]] = []
        with open(Path(self.source, self.NAV_JSON), "rb") as f:
            for d in json.load(f):
                self.nav_trees.append(
                    navnode_to_tree(
                        NavNode.from_dict(d),
                        self.source.as_posix()
                    )
                )
