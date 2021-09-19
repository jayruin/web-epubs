from pathlib import Path
import shutil
from typing import Optional

from .epub_resource import EPUBResource
from core.templates import XHTMLTemplate


class EPUBResourceManager:
    def __init__(self, root: Path) -> None:
        self.root: Path = root
        self.resources: dict[Path, EPUBResource] = {}
        self.xhtml_to_html: dict[Path, Path] = {}
        self.clear()

    def clear(self) -> None:
        """
        Clear all resources and delete already added files.
        """
        self.resources.clear()
        self.xhtml_to_html.clear()
        shutil.rmtree(self.root, ignore_errors=True)
        self.root.mkdir(parents=True, exist_ok=True)

    def import_resources(
        self,
        path: Path,
        root: Optional[Path] = None
    ) -> None:
        """
        Recursively copy resource files from the given path starting from root.
        If root is not specified, then it defaults to path.
        Files beginning with underscore _ are skipped.
        Handling of HTML files is deferred until convert_html is called.
        """
        if root is None:
            root = path
        assert root.is_dir()
        if path.is_file():
            resource_path = path.relative_to(root)
            if path.name.startswith("_"):
                return
            elif path.suffix == ".html":
                xhtml_resource = resource_path.with_suffix(".xhtml")
                self.resources[xhtml_resource] = EPUBResource(xhtml_resource)
                destination = Path(self.root, xhtml_resource)
                self.xhtml_to_html[destination] = path
            else:
                self.resources[resource_path] = EPUBResource(resource_path)
                destination = Path(self.root, resource_path)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
        elif path.is_dir():
            for child_path in path.iterdir():
                self.import_resources(child_path, root)

    def convert_html(self, xhtml_template: XHTMLTemplate) -> None:
        """
        Convert seen HTML files into XHTML files using xhtml_template.
        """
        for xhtml_file, html_file in self.xhtml_to_html.items():
            xhtml_file.parent.mkdir(parents=True, exist_ok=True)
            xhtml_template.fill(html_file, xhtml_file)

    def add_id_counts(self) -> None:
        """
        Add id_count values for all resources such that every resource
        has a unique manifest_id.
        """
        for count, path in enumerate(
            sorted(
                self.resources,
                key=lambda p: p.as_posix()
            ),
            start=1
        ):
            self.resources[path].id_count = count
