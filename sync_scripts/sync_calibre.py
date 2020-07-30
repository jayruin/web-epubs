import os
import pathlib
import sys

root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(root)
os.chdir(root)

from calibrecli import calibredb  # noqa E402
from template_scripts._shared.metadata import Metadata  # noqa E402


# PORTABLE = "/Calibre Portable/Calibre"
# LIBRARY = "/Calibre Portable/Calibre Library"
PORTABLE = ""
LIBRARY = None


def main():
    new_books = []
    for arg in sys.argv[1:]:
        metadata = Metadata.from_json_path(f"html/{arg}/_metadata.json")
        search_terms = []
        search_terms.append(f"title:{metadata.title}")
        search_terms.append(f"author:{metadata.author}")
        ebook_file = f"./epub/{arg}.epub"
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
                ebook_file_=ebook_file
            )
        else:
            print(f"Skipping {arg} due to ambiguous metadata")
    if new_books:
        calibredb.add(new_books)


if __name__ == "__main__":
    main()
