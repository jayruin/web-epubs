from pathlib import Path

from .xhtml_template import XHTMLTemplate


class EPUB3Template(XHTMLTemplate):
    def fill(self, html_file: Path, xhtml_file: Path) -> None:
        pass
