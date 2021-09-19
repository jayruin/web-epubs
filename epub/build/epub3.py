from pathlib import Path
import shutil

from core.documents import ContainerXML, MimetypeFile
from core.project import EPUBProject, EPUBResourceManager
from core.settings import Settings
from core.templates import EPUB3Template
from epub import make_project_argparser


class Builder:
    def __init__(
        self,
        settings: Settings,
        project_name: str
    ) -> None:
        self.builder_name: str = "epub3"

        self.settings: Settings = settings

        self.source: Path = Path(settings.projects_directory, project_name)
        self.destination: Path = Path(
            settings.expanded_epubs_directory,
            self.builder_name,
            project_name
        )

        self.project: EPUBProject = EPUBProject(self.source)
        self.resource_manager: EPUBResourceManager = EPUBResourceManager(
            Path(
                self.destination,
                self.project.RESOURCES_DIRECTORY
            )
        )

        self.css_files: list[Path] = self.project.epub_metadata.css
        self.js_files: list[Path] = self.project.epub_metadata.js

    def clear(self) -> None:
        shutil.rmtree(self.destination, ignore_errors=True)
        self.destination.mkdir(parents=True, exist_ok=True)
        self.resource_manager.clear()

    def build(self, bundles: list[Path]) -> None:
        self.clear()
        self.write_mimetype_file()
        self.fill_meta_inf()
        self.import_resources(bundles)
        self.convert_html()

    def write_mimetype_file(self) -> None:
        mimetype_file = MimetypeFile()
        mimetype_file.epub3(Path(self.destination, self.project.MIMETYPE_FILE))

    def fill_meta_inf(self) -> None:
        meta_inf_directory = Path(self.destination, self.project.META_INF)
        meta_inf_directory.mkdir()

        container_xml = ContainerXML(
            Path(self.project.RESOURCES_DIRECTORY, self.project.PACKAGE_OPF)
        )
        container_xml.epub3(
            Path(meta_inf_directory, self.project.CONTAINER_XML)
        )

    def import_resources(self, bundles: list[Path]) -> None:
        for bundle in bundles:
            self.resource_manager.import_resources(bundle)
        self.resource_manager.import_resources(self.source)
        found_css_files: set[Path] = set()
        found_js_files: set[Path] = set()
        for file in self.resource_manager.resources:
            if file.suffix == ".css":
                found_css_files.add(file)
            if file.suffix == ".js":
                found_js_files.add(file)
        remaining_css_files = found_css_files - set(self.css_files)
        remaining_js_files = found_js_files - set(self.js_files)
        self.css_files.extend(
            sorted(
                remaining_css_files,
                key=lambda p: p.as_posix()
            )
        )
        self.js_files.extend(
            sorted(
                remaining_js_files,
                key=lambda p: p.as_posix()
            )
        )

    def convert_html(self) -> None:
        template = EPUB3Template(self.css_files, self.js_files)
        self.resource_manager.convert_html(template)


def main() -> None:
    description = "Build epub3"
    parser = make_project_argparser(description)
    parser.add_argument(
        "-b", "--bundles",
        nargs="+",
        default=[],
        type=Path
    )
    args = parser.parse_args()
    settings = Settings.from_namespace(args)
    builder = Builder(settings, args.projects[0])
    builder.build(args.bundles)


if __name__ == "__main__":
    main()
