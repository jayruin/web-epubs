import json
import multiprocessing
import os.path
from pathlib import Path
import sys

from core import constants
from core.argparsers import parser_projects_only
from core.epubs import EPUBCheck, EPUBFile


def main():
    ec = EPUBCheck(
        constants.EPUBCHECK_DOWNLOAD_URL,
        constants.EPUBCHECK_ROOT_DIR,
        constants.EPUBCHECK_LOCAL_ZIP,
        constants.JAVA_EXECUTABLE
    )
    if not ec.exists():
        sys.exit("EPUBCheck not installed!")

    module_name = "epub.zipping"
    description = "Zip ePub contents into a single .epub file."
    parser = parser_projects_only(module_name, description, False)
    args = parser.parse_args()
    epubs_to_build = args.projects

    epubs_to_build = [
        name if len(Path(name).parts) != 1
        else os.path.join(constants.EPUB_DIRECTORY, name)
        for name in epubs_to_build
    ]

    with multiprocessing.Pool() as pool:
        pool.map(EPUBFile.zip_directory, epubs_to_build)
    summary = {
        "fatals": 0,
        "errors": 0,
        "warnings": 0
    }
    for name in epubs_to_build:
        result = ec.check(f"{name}.epub", f"{name}.txt")
        summary["fatals"] += result.fatals
        summary["errors"] += result.errors
        summary["warnings"] += result.warnings
    with open(constants.EPUBCHECK_SUMMARY_JSON, "w", encoding="utf-8") as f:
        f.write(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()
