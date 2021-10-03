from pathlib import Path

from .anchor import Anchor
from .epub_metadata import EPUBMetadata
from .tree import Tree
from core.deserialize import read_any, read_epub_metadata, read_nav


class EPUBProject:
    CONTAINER_XML: str = "container.xml"
    COVER_CSS_CLASS: str = "cover-image"
    COVER_XHTML: str = "_cover.xhtml"
    META_INF = "META-INF"
    METADATA_JSON: str = "_metadata.json"
    MIMETYPE_FILE: str = "mimetype"
    NAV_JSON: str = "_nav.json"
    NAVIGATION_DOCUMENT: str = "_nav.xhtml"
    NCX_DOCUMENT: str = "_toc.ncx"
    PACKAGE_DOCUMENT: str = "_package.opf"
    RESOURCES_DIRECTORY: str = "OEBPS"
    SUPPORTED_SUFFIXES: list[str] = [".json", ".yaml", ".yml"]

    def __init__(self, root: Path) -> None:
        self.root: Path = root
        self.name: str = root.stem

        self.epub_metadata: EPUBMetadata = read_any(
            Path(self.root, self.METADATA_JSON),
            read_epub_metadata,
            self.SUPPORTED_SUFFIXES
        )

        self.nav_trees: list[Tree[Anchor]] = read_any(
            Path(self.root, self.NAV_JSON),
            read_nav,
            self.SUPPORTED_SUFFIXES
        )
