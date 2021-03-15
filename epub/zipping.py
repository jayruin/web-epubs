import argparse
import json
import multiprocessing
import os.path
from pathlib import Path
import sys

from core import constants
from core.argparsers import parser_projects_only
from core.epubs import EPUBCheck, EPUBFile
from core.files.writers import Utf8Writer


def main():
    module_name = "epub.zipping"
    description = "Zip ePub contents into a single .epub file."
    parent_parser = parser_projects_only(module_name, description, True)
    parser = argparse.ArgumentParser(parents=[parent_parser])
    parser.prog = parent_parser.prog
    parser.add_argument(
        "-c",
        "--compress-level",
        help=" ".join(
            [
                "Compression level to use for the output .epub file.",
                "Default value is 0: no compression."
            ]
        ),
        nargs="?",
        default=0,
        type=int,
        choices=range(10)
    )
    parser.add_argument(
        "-s",
        "--skip-epubcheck",
        help=" ".join(
            [
                "Skip epubcheck for the output .epub files.",
                "Default is false.",
                "It is highly recommended to run epubcheck."
            ]
        ),
        action="store_true"
    )
    args = parser.parse_args()
    epubs_to_build = args.projects

    epubs_to_build = [
        name if len(Path(name).parts) != 1
        else os.path.join(constants.EPUB_DIRECTORY, name)
        for name in epubs_to_build
    ]

    with multiprocessing.Pool() as pool:
        pool.starmap(
            EPUBFile.zip_directory,
            [(epub, args.compress_level) for epub in epubs_to_build]
        )

    if not args.skip_epubcheck:
        ec = EPUBCheck(
            constants.EPUBCHECK_DOWNLOAD_URL,
            constants.EPUBCHECK_ROOT_DIR,
            constants.EPUBCHECK_LOCAL_ZIP,
            constants.JAVA_EXECUTABLE
        )
        if not ec.exists():
            sys.exit("EPUBCheck not installed!")
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
        writer = Utf8Writer()
        writer.write(
            constants.EPUBCHECK_SUMMARY_JSON,
            json.dumps(summary, indent=4)
        )


if __name__ == "__main__":
    main()
