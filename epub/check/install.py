from io import BytesIO
import json
from pathlib import Path
import shutil
from typing import Optional
import urllib.request
from zipfile import ZipFile

from app import Settings
from core.constants import EPUBCHECK_RELEASES_URL
from core.runner import make_project_argparser


def install_epubcheck(settings: Settings) -> None:
    # Delete previous installation
    shutil.rmtree(settings.epubcheck_directory, ignore_errors=True)
    settings.epubcheck_directory.mkdir(parents=True, exist_ok=True)

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
    with urllib.request.urlopen(zip_download_url) as response:
        with ZipFile(BytesIO(response.read())) as z:
            for zip_info in z.infolist():
                if not zip_info.is_dir():
                    destination = Path(
                        settings.epubcheck_directory,
                        *Path(zip_info.filename).parts[1:]
                    )
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(zip_info) as zip_file:
                        with open(destination, "wb") as f:
                            f.write(zip_file.read())


def main() -> None:
    description = "Install EPUBCheck"
    parser = make_project_argparser(description)
    args = parser.parse_args()
    settings = Settings.from_namespace(args)
    install_epubcheck(settings)


if __name__ == "__main__":
    main()
