from __future__ import annotations
import os
from pathlib import Path
import zipfile
from zipfile import ZipFile


class EPUBFile:
    def __init__(
        self,
        directory_str: str,
        destination_str: str,
        compress_level: int = 0
    ) -> None:
        self.directory_path = Path(directory_str)
        self.destination_path = Path(destination_str)
        with ZipFile(
            self.destination_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=compress_level
        ) as z:
            z.write(
                Path(self.directory_path, "mimetype"),
                "mimetype", zipfile.ZIP_STORED
            )
            self._add(z, self.directory_path)

    def _add(
        self,
        z: ZipFile,
        file_or_dir: Path
    ) -> None:
        if file_or_dir.is_file() and file_or_dir.name != "mimetype":
            z.write(
                file_or_dir,
                str(file_or_dir.relative_to(self.directory_path)),
                zipfile.ZIP_STORED
            )
        elif file_or_dir.is_dir():
            with os.scandir(file_or_dir) as it:
                for entry in it:
                    self._add(z, Path(entry.path))

    @classmethod
    def zip_directory(
        cls,
        directory_str: str,
        compress_level: int = 0
    ) -> EPUBFile:
        return cls(directory_str, f"{directory_str}.epub", compress_level)
