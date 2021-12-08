from pathlib import Path
import shutil

import markdown

from core.constants import Encoding
from core.documents.sgml import get_doctype_html
from plugins.pagimg.navigation import make_title


def convert(source: Path, destination: Path, copy: bool) -> None:
    if source.is_file():
        if source.suffix == ".md":
            md_to_html(source, destination)
        else:
            if copy:
                shutil.copy(source, destination)
    elif source.is_dir():
        destination.mkdir(exist_ok=True)
        for child_path in source.iterdir():
            convert(child_path, Path(destination, child_path.name), copy)


def md_to_html(source: Path, destination: Path) -> None:
    extensions = ["sane_lists"]
    with open(source, "r", encoding=Encoding.UTF_8.value) as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content, extensions=extensions)
    title = make_title(source.stem)
    destination.with_suffix(".html").write_text(
        "\n".join(
            [
                get_doctype_html(False),
                f"<title>{title}</title>",
                html_content
            ]
        ),
        encoding=Encoding.UTF_8.value
    )
