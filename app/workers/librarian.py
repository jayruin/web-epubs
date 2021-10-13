from .app_worker import AppWorker


class Librarian(AppWorker):
    def get_projects(self) -> list[str]:
        return [
            path.name
            for path in self.settings.projects_directory.iterdir()
            if path.is_dir()
        ]

    def get_expanded_epubs(self) -> dict[str, list[str]]:
        return {
            epub_type_path.stem: list(
                path.stem
                for path in epub_type_path.iterdir()
                if path.is_dir()
            )
            for epub_type_path
            in self.settings.expanded_epubs_directory.iterdir()
            if epub_type_path.is_dir()
        }

    def get_packaged_epubs(self) -> dict[str, list[str]]:
        return {
            epub_type_path.stem: list(
                ".".join(path.stem.split(".")[:-1])
                for path in epub_type_path.iterdir()
                if path.is_file()
                and path.suffix == ".epub"
                and path.stem.endswith(f".{epub_type_path.stem}")
            )
            for epub_type_path
            in self.settings.packaged_epubs_directory.iterdir()
            if epub_type_path.is_dir()
        }
