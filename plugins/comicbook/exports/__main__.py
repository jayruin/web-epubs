import argparse
import json
from pathlib import Path

from core.files.readers import Utf8Reader
from plugins.comicbook.comicbook_project import ComicbookProject


settings_file = "./plugins/comicbook/exports/settings.json"
reader = Utf8Reader()
plugin_settings = json.loads(reader.read(settings_file))


prog = "python -m plugins.comicbook.exports"
description = "Exports a comic book project."
parser = argparse.ArgumentParser(prog=prog, description=description)
parser.add_argument(
    "destination",
    help=" ".join(
        [
            "The destination path for the export.",
            "Should be a cbz file."
        ]
    ),
    type=Path
)
parser.add_argument(
    "project",
    help=" ".join(
        [
            "Project to export.",
            "Project should be a subdirectory of the html directory."
        ]
    )
)
parser.add_argument(
    "volume",
    help=" ".join(
        [
            "Volume in the project to export.",
            "Volume should be a subdirectory of the project directory.",
            "If not specified, the entire project will be exported."
        ]
    ),
    nargs="?"
)
parser.add_argument(
    "chapter",
    help=" ".join(
        [
            "Chapter in the volume to export.",
            "Chapter should be a subdirectory of the volume directory.",
            "If not specified, the entire volume will be exported."
        ]
    ),
    nargs="?"
)
parser.add_argument(
    "-c",
    "--compress-level",
    help=" ".join(
        [
            "Compression level to use for the destination .cbz file."
        ]
    ),
    nargs="?",
    type=int,
    choices=range(10)
)
args = parser.parse_args()

comicbook_project = ComicbookProject(args.project)
comicbook_project.export(
    args.destination,
    args.volume,
    args.chapter,
    args.compress_level
)
