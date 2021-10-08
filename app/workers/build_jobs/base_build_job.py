from abc import ABC, abstractmethod
from pathlib import Path
import shutil
from typing import Optional

from .epub_type import EPUBType
from .epub_version import EPUBVersion
from app.settings import Settings
from core.cover import fill_blank_cover
from core.documents import (
    ContainerXML,
    CoverXHTML,
    EPUB2PackageDocument,
    EPUB3PackageDocument,
    MimetypeFile,
    NavigationDocument,
    NCXDocument
)
from core.project import Anchor, EPUBProject, EPUBResource, EPUBResourceManager
from core.templates import EPUB2Template, EPUB3Template


class BaseBuildJob(ABC):
    def __init__(
        self,
        settings: Settings,
        project_name: str,
        bundles: list[str]
    ) -> None:
        self._settings: Settings = settings

        self._bundles: list[str] = bundles

        self._source: Path = Path(settings.projects_directory, project_name)
        self._destination: Path = Path(
            settings.expanded_epubs_directory,
            self.epub_type.value,
            project_name
        )

        self._project: EPUBProject = EPUBProject(self._source)
        self._resource_manager: EPUBResourceManager = EPUBResourceManager(
            Path(
                self._destination,
                self._project.RESOURCES_DIRECTORY
            )
        )

        self._css_files: list[Path] = self._project.epub_metadata.css
        self._js_files: list[Path] = self._project.epub_metadata.js

        self._progression: list[Path] = []

        self._landmarks: list[Anchor] = []

    @classmethod
    @property
    @abstractmethod
    def epub_type(cls) -> EPUBType:
        pass

    @classmethod
    @property
    @abstractmethod
    def epub_version(cls) -> EPUBVersion:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    def _clear(self) -> None:
        shutil.rmtree(self._destination, ignore_errors=True)
        self._destination.mkdir(parents=True, exist_ok=True)
        self._resource_manager.clear()

    def _write_mimetype_file(
        self,
        epub_version: Optional[EPUBVersion] = None
    ) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        document = MimetypeFile()
        document_path = Path(self._destination, self._project.MIMETYPE_FILE)

        if epub_version is EPUBVersion.EPUB2:
            document.epub2(document_path)
        elif epub_version is EPUBVersion.EPUB3:
            document.epub3(document_path)

    def _fill_meta_inf(
        self,
        epub_version: Optional[EPUBVersion] = None
    ) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        meta_inf_directory = Path(self._destination, self._project.META_INF)
        meta_inf_directory.mkdir()

        document = ContainerXML(
            Path(
                self._project.RESOURCES_DIRECTORY,
                self._project.PACKAGE_DOCUMENT
            )
        )
        document_path = Path(meta_inf_directory, self._project.CONTAINER_XML)

        if epub_version is EPUBVersion.EPUB2:
            document.epub2(document_path)
        elif epub_version is EPUBVersion.EPUB3:
            document.epub3(document_path)

    def _import_resources(self) -> None:
        for bundle in self._bundles:
            self._resource_manager.import_resources(
                Path(self._settings.bundles_directory, bundle)
            )
        self._resource_manager.import_resources(self._source)
        found_css_files: set[Path] = set()
        found_js_files: set[Path] = set()
        for file in self._resource_manager.resources:
            if file.suffix == ".css":
                found_css_files.add(file)
            elif file.suffix == ".js":
                found_js_files.add(file)
        remaining_css_files = found_css_files - set(self._css_files)
        remaining_js_files = found_js_files - set(self._js_files)
        self._css_files.extend(
            sorted(
                remaining_css_files,
                key=lambda p: p.as_posix()
            )
        )
        self._js_files.extend(
            sorted(
                remaining_js_files,
                key=lambda p: p.as_posix()
            )
        )

    def _convert_html(
        self,
        epub_version: Optional[EPUBVersion] = None
    ) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        if epub_version is EPUBVersion.EPUB2:
            template = EPUB2Template(
                self._css_files,
                self._resource_manager.root
            )
        elif epub_version is EPUBVersion.EPUB3:
            template = EPUB3Template(
                self._css_files,
                self._js_files,
                self._resource_manager.root
            )
        self._resource_manager.convert_html(template)
        for xhtml_file in self._resource_manager.xhtml_to_html:
            self._resource_manager.resources[
                xhtml_file.relative_to(self._resource_manager.root)
            ].properties = "scripted"

    def _write_cover(self, epub_version: Optional[EPUBVersion] = None) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        if not self._project.epub_metadata.cover:
            default_cover = Path("_cover.jpg")
            fill_blank_cover(Path(self._resource_manager.root, default_cover))
            self._project.epub_metadata.cover = default_cover
        self._resource_manager.resources[
            self._project.epub_metadata.cover
        ] = EPUBResource(
            self._project.epub_metadata.cover,
            properties="cover-image"
        )
        document = CoverXHTML(self._project.epub_metadata.cover)
        document_path = Path(
            self._resource_manager.root,
            self._project.COVER_XHTML
        )

        if epub_version is EPUBVersion.EPUB2:
            document.epub2(document_path)
        elif epub_version is EPUBVersion.EPUB3:
            document.epub3(document_path)

        cover_xhtml_path = Path(self._project.COVER_XHTML)
        self._resource_manager.resources[cover_xhtml_path] = EPUBResource(
            cover_xhtml_path
        )
        self._progression.append(cover_xhtml_path)
        self._landmarks.append(Anchor("Cover", cover_xhtml_path, "cover"))

    def _write_navigation_document(
        self,
        epub_version: Optional[EPUBVersion] = None
    ) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        navigation = Path(self._project.NAVIGATION_DOCUMENT)
        self._resource_manager.resources[navigation] = EPUBResource(
            navigation,
            properties="nav"
        )
        self._landmarks.append(Anchor("Table of Contents", navigation, "toc"))
        self._progression.append(navigation)
        bodymatter_progression: list[Path] = []
        for nav_tree in self._project.nav_trees:
            for anchor in nav_tree.depth_first_traversal():
                if len(anchor.href.name.split("#")) == 1:
                    bodymatter_progression.append(anchor.href)
        if len(bodymatter_progression) > 0:
            self._landmarks.append(
                Anchor(
                    "Begin Reading",
                    bodymatter_progression[0],
                    "bodymatter"
                )
            )
        self._progression.extend(bodymatter_progression)

        document = NavigationDocument(
            self._project.nav_trees,
            self._landmarks
        )
        document_path = Path(
            self._resource_manager.root,
            self._project.NAVIGATION_DOCUMENT
        )

        if epub_version is EPUBVersion.EPUB2:
            document.epub2(document_path)
        elif epub_version is EPUBVersion.EPUB3:
            document.epub3(document_path)

    def _write_ncx_document(self) -> None:
        ncx = Path(self._project.NCX_DOCUMENT)
        self._resource_manager.resources[ncx] = EPUBResource(ncx)
        document = NCXDocument(
            self._project.nav_trees,
            self._project.epub_metadata.identifier,
            self._project.epub_metadata.title
        )
        document_path = Path(self._resource_manager.root, ncx)
        document.epub2(document_path)

    def _write_package_document(
        self,
        epub_version: Optional[EPUBVersion] = None
    ) -> None:
        if epub_version is None:
            epub_version = self.epub_version

        self._resource_manager.add_id_counts()

        if epub_version is EPUBVersion.EPUB2:
            ncx = Path(self._project.NCX_DOCUMENT)
            document = EPUB2PackageDocument(
                self._project.epub_metadata,
                self._resource_manager.resources,
                self._progression,
                ncx,
                self._landmarks
            )
            document_path = Path(
                self._resource_manager.root,
                self._project.PACKAGE_DOCUMENT
            )
            document.epub2(document_path)
        elif epub_version is EPUBVersion.EPUB3:
            document = EPUB3PackageDocument(
                self._project.epub_metadata,
                self._resource_manager.resources,
                self._progression
            )
            document_path = Path(
                self._resource_manager.root,
                self._project.PACKAGE_DOCUMENT
            )
            document.epub3(document_path)
