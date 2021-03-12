import argparse
import json
from pathlib import Path

from core.files.readers import Utf8Reader
from plugins.comicbook.comicbook_project import ComicbookProject


settings_file = "./plugins/comicbook/imports/settings.json"
reader = Utf8Reader()
plugin_settings = json.loads(reader.read(settings_file))


parser = argparse.ArgumentParser()
parser.add_argument(
    "project",
    help=" ".join(
        [
            "Project to add to.",
            "Project should be a subdirectory of the html directory."
        ]
    )
)
parser.add_argument(
    "volume",
    help=" ".join(
        [
            "Volume in the project to add to.",
            "Volume should be a subdirectory of the project directory."
        ]
    )
)
parser.add_argument(
    "chapter",
    help=" ".join(
        [
            "Chapter to add.",
            "Chapter is a path to a directory of images or a .cbz file."
        ]
    )
)
parser.add_argument(
    "-n",
    "--new-volume",
    action="store_true",
    help=" ".join(
        [
            "Specifies that the volume does not currently exist.",
            "A new volume will be created."
        ]
    )
)
args = parser.parse_args()

comicbook_project = ComicbookProject(args.project)
if args.new_volume:
    comicbook_project.create_volume(args.volume, Path(args.chapter).name)
comicbook_project.import_chapter(args.volume, Path(args.chapter))
