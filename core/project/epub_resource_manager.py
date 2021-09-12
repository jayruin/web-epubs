from pathlib import Path
import shutil

from core.templates import XHTMLTemplate


class EPUBResourceManager:
    def __init__(self, root: Path) -> None:
        self.root: Path = root
        self.resources: set[Path] = set()
        self.clear()

    def clear(self) -> None:
        self.resources.clear()
        shutil.rmtree(self.root, ignore_errors=True)
        self.root.mkdir(parents=True, exist_ok=True)

    def import_resources(
        self,
        root: Path,
        path: Path,
        xhtml_template: XHTMLTemplate
    ) -> None:
        assert root.is_dir()
        if path.is_file():
            resource = path.relative_to(root)
            if path.name.startswith("_"):
                return
            elif path.suffix == ".html":
                converted_resource = resource.with_suffix(".xhtml")
                self.resources.add(converted_resource)
                destination = Path(self.root, converted_resource)
                destination.parent.mkdir(parents=True, exist_ok=True)
                xhtml_template.fill(path, destination)
            else:
                self.resources.add(resource)
                destination = Path(self.root, resource)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
        elif path.is_dir():
            for child_path in path.iterdir():
                self.import_resources(root, child_path, xhtml_template)
