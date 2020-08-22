import multiprocessing
import sys

from core.epubs import EPUBFile  # noqa E402
from core.epubs import EPUBCheck  # noqa E402


DOWNLOAD_LINK = "https://api.github.com/repos/w3c/epubcheck/releases/latest"
LOCAL_ZIP = "./epubcheck.zip"
ROOT_DIR = "./epubcheck"


ec = EPUBCheck(DOWNLOAD_LINK, ROOT_DIR, LOCAL_ZIP, "java")
ec.install()

epubs_to_build = sys.argv[1:]
if not epubs_to_build:
    epubs_to_build = [line.strip() for line in sys.stdin]

with multiprocessing.Pool() as pool:
    pool.map(EPUBFile.zip_directory, epubs_to_build)
for name in epubs_to_build:
    ec.check(f"{name}.epub", f"{name}.txt")
