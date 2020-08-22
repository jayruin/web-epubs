import multiprocessing
import os
import pathlib
import sys

root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(root)
os.chdir(root)

from epub_scripts.epub import EPUB  # noqa E402
from core.epub.epub_check import EPUBCheck  # noqa E402


DOWNLOAD_LINK = "https://api.github.com/repos/w3c/epubcheck/releases/latest"
LOCAL_ZIP = "./epubcheck.zip"
ROOT_DIR = "./epubcheck"


def build(
    name: str
) -> None:
    EPUB(name, f"{name}.epub")


def main():
    ec = EPUBCheck(DOWNLOAD_LINK, ROOT_DIR, LOCAL_ZIP, "java")
    ec.install()

    epubs_to_build = sys.argv[1:]
    if not epubs_to_build:
        epubs_to_build = [line.strip() for line in sys.stdin]

    pool = multiprocessing.Pool()
    pool.map(build, epubs_to_build)
    for name in epubs_to_build:
        ec.check(f"{name}.epub", f"{name}.txt")


if __name__ == "__main__":
    main()
