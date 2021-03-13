import json

from core.argparsers import parser_projects_only
from core.config.metadata import Metadata
from core.files.readers import Utf8Reader
from plugins.calibre.cli import calibredb


settings_file = "./plugins/calibre/sync/settings.json"
reader = Utf8Reader()
plugin_settings = json.loads(reader.read(settings_file))
PORTABLE = plugin_settings["PORTABLE"]
LIBRARY = plugin_settings["LIBRARY"]


module_name = "plugins.calibre.sync"
description = " ".join(
    [
        "Sync projects with Calibre.",
        "Make sure you have Calibre installed."
    ]
)
parser = parser_projects_only(module_name, description, False)
args = parser.parse_args()


new_books = []
for project in args.projects:
    metadata = Metadata.from_json_path(f"html/{project}/_metadata.json")
    search_terms = []
    search_terms.append(f"title:{metadata.title}")
    search_terms.append(f"author:{metadata.author}")
    ebook_file = f"./epub/{project}.epub"
    book_ids = calibredb.search(
        search_expression_=" ".join(search_terms),
        portable=PORTABLE,
        with_library_=LIBRARY
    )
    if not book_ids:
        new_books.append(ebook_file)
    elif len(book_ids) == 1:
        calibredb.add_format(
            id_=book_ids[0],
            ebook_file_=ebook_file,
            portable=PORTABLE,
            with_library_=LIBRARY
        )
    else:
        print(f"Skipping {project} due to ambiguous metadata")
if new_books:
    calibredb.add(
        files_=new_books,
        portable=PORTABLE,
        with_library_=LIBRARY
    )
