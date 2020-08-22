import multiprocessing
import os.path
from pathlib import Path
import sys

from core import constants
from core.epubs import EPUBCheck, EPUBFile


DOWNLOAD_LINK = "https://api.github.com/repos/w3c/epubcheck/releases/latest"
LOCAL_ZIP = "./epubcheck.zip"
ROOT_DIR = "./epubcheck"
JAVA = "java"


ec = EPUBCheck(DOWNLOAD_LINK, ROOT_DIR, LOCAL_ZIP, JAVA)
ec.install()

epubs_to_build = sys.argv[1:]
if not epubs_to_build:
    epubs_to_build = [line.strip() for line in sys.stdin]
epubs_to_build = [
    name if len(Path(name).parts) != 1
    else os.path.join(constants.EPUB_DIRECTORY, name)
    for name in epubs_to_build
]

with multiprocessing.Pool() as pool:
    pool.map(EPUBFile.zip_directory, epubs_to_build)
for name in epubs_to_build:
    ec.check(f"{name}.epub", f"{name}.txt")
