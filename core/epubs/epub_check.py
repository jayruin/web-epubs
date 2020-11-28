import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.request
from zipfile import ZipFile

from .epub_check_results import EPUBCheckResults


class EPUBCheck:
    def __init__(
        self,
        web_url: str,
        root_path_str: str,
        local_zip_str: str,
        java: str
    ) -> None:
        self.web_url: str = web_url
        self.root_path: Path = Path(root_path_str)
        self.local_zip_path: Path = Path(local_zip_str)
        self.java = java

    def _get_latest_zip_url(
        self
    ) -> None:
        with urllib.request.urlopen(self.web_url) as response:
            json_response = json.load(response)
            for asset in json_response["assets"]:
                if asset["browser_download_url"].endswith(".zip"):
                    self.web_url = asset["browser_download_url"]
                    return

    def _download_zip(
        self
    ) -> None:
        with urllib.request.urlopen(self.web_url) as response:
            with open(self.local_zip_path, "wb") as f:
                f.write(response.read())

    def _unzip(
        self
    ) -> None:
        shutil.rmtree(self.root_path, ignore_errors=True)
        with ZipFile(self.local_zip_path, "r") as z:
            z.extractall(self.root_path)
        root_dir = Path(
            self.root_path,
            Path(self.web_url).with_suffix("").name
        )
        with os.scandir(root_dir) as it:
            for entry in it:
                p = Path(entry)
                p.rename(Path(p.parents[1], p.name))
        os.rmdir(root_dir)
        os.remove(self.local_zip_path)

    def install(
        self
    ) -> None:
        self._get_latest_zip_url()
        self._download_zip()
        self._unzip()

    def check(
        self,
        epub_file: str,
        output_file: str
    ) -> EPUBCheckResults:
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(
                [
                    self.java,
                    "-jar",
                    str(Path(self.root_path, "epubcheck.jar")),
                    epub_file
                ],
                stdout=f,
                stderr=f
            )
        return EPUBCheckResults.from_txt(
            Path(epub_file).with_suffix(".txt")
        )

    def exists(
        self
    ) -> bool:
        return self.root_path.exists()
