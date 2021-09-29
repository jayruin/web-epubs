from io import BytesIO
from collections.abc import Generator
from contextlib import contextmanager, ExitStack
import json
from pathlib import Path
import shutil
from typing import Optional
import urllib.request
from zipfile import ZipFile

from tqdm import tqdm

from .app_worker import AppWorker
from core.constants import EPUBCHECK_RELEASES_URL


class Installer(AppWorker):
    def install_epubcheck(self) -> None:
        # Delete previous installation
        shutil.rmtree(self.settings.epubcheck_directory, ignore_errors=True)
        self.settings.epubcheck_directory.mkdir(parents=True, exist_ok=True)

        # Find download url for zip
        zip_download_url: Optional[str] = None
        with urllib.request.urlopen(EPUBCHECK_RELEASES_URL) as response:
            json_response = json.load(response)
            for asset in json_response["assets"]:
                if asset["browser_download_url"].endswith(".zip"):
                    zip_download_url = asset["browser_download_url"]
                    break
        if zip_download_url is None:
            raise Exception("Could not find zip download URL!")

        # Download zip file into memory and extract to directory
        with download_to_memory(zip_download_url, show_progress=True) as data:
            with ZipFile(data) as z:
                for zip_info in z.infolist():
                    if not zip_info.is_dir():
                        destination = Path(
                            self.settings.epubcheck_directory,
                            *Path(zip_info.filename).parts[1:]
                        )
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        with z.open(zip_info) as zip_file:
                            with open(destination, "wb") as f:
                                f.write(zip_file.read())


@contextmanager
def download_to_memory(
    url: str,
    show_progress: bool = False
) -> Generator[BytesIO, None, None]:
    stack = ExitStack()
    try:
        response = stack.enter_context(urllib.request.urlopen(url))
        try:
            total = int(response.getheader("Content-Length"))
        except (TypeError, ValueError):
            total = None
        if show_progress:
            response = stack.enter_context(
                tqdm.wrapattr(
                    response,
                    "read",
                    total=total
                )
            )
        memory_stream = stack.enter_context(BytesIO())
        shutil.copyfileobj(response, memory_stream)
        yield memory_stream
    finally:
        stack.close()
