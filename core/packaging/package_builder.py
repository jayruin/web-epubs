from abc import ABC, abstractmethod
import shutil
from typing import Type

from core.files.readers import TextReader, Utf8Reader
from core.files.writers import TextWriter, Utf8Writer
from core.formatters import (
    CsslinksFormatter,
    LanguagesFormatter,
    ManifestitemsFormatter,
    NavlisFormatter,
    SpineitemrefsFormatter
)
from .package_contents import PackageContents


class PackageBuilder(ABC):
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
        self.src: str = src
        self.dst: str = dst
        self.template_dir: str = template_dir

        self.package_contents: PackageContents = PackageContents(
            src=src,
            template_dir=template_dir
        )
        self.csslinks_formatter: CsslinksFormatter
        self.languages_formatter: LanguagesFormatter
        self.manifestitems_formatter: ManifestitemsFormatter
        self.navlis_formatter: NavlisFormatter
        self.spineitemrefs_formatter: SpineitemrefsFormatter

        self.csslinks_formatter = CsslinksFormatter(
            self.package_contents
        )
        self.languages_formatter = LanguagesFormatter(
            self.package_contents
        )
        self.manifestitems_formatter = ManifestitemsFormatter(
            self.package_contents
        )
        self.navlis_formatter = NavlisFormatter(
            self.package_contents
        )
        self.spineitemrefs_formatter = SpineitemrefsFormatter(
            self.package_contents
        )

        self.reader: Type[TextReader] = Utf8Reader()
        self.writer: Type[TextWriter] = Utf8Writer()

        shutil.rmtree(self.dst, ignore_errors=True)

    @abstractmethod
    def build(
        self
    ) -> None:
        pass
