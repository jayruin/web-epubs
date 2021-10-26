from pathlib import Path

from .anchor import Anchor
from .epub_metadata import EPUBMetadata
from core.datastructures import Tree
from core.deserialize import read_any, read_epub_metadata, read_nav


class EPUBProject:
    CONTAINER_XML: str = "container.xml"
    COVER_CSS_CLASS: str = "cover-image"
    COVER_XHTML: str = "_cover.xhtml"
    META_INF = "META-INF"
    METADATA: str = "_metadata"
    MIMETYPE_FILE: str = "mimetype"
    NAV: str = "_nav"
    NAVIGATION_DOCUMENT: str = "_nav.xhtml"
    NCX_DOCUMENT: str = "_toc.ncx"
    PACKAGE_DOCUMENT: str = "_package.opf"
    RESOURCES_DIRECTORY: str = "OEBPS"
    SUPPORTED_SUFFIXES: list[str] = [".json", ".yaml", ".yml"]

    def __init__(self, root: Path) -> None:
        self.root: Path = root
        self.name: str = root.stem

        self.epub_metadata: EPUBMetadata = read_any(
            Path(self.root, self.METADATA),
            read_epub_metadata,
            self.SUPPORTED_SUFFIXES
        )

        self.nav_trees: list[Tree[Anchor]] = read_any(
            Path(self.root, self.NAV),
            read_nav,
            self.SUPPORTED_SUFFIXES
        )
