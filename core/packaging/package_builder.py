from abc import ABC, abstractmethod
import shutil
from typing import Type

from .package_contents import PackageContents
from core.files.readers.text_reader import TextReader
from core.files.readers.utf8_reader import Utf8Reader
from core.files.writers.text_writer import TextWriter
from core.files.writers.utf8_writer import Utf8Writer
from core.formatters.creators_formatter import CreatorsFormatter
from core.formatters.csslinks_formatter import CsslinksFormatter
from core.formatters.languages_formatter import LanguagesFormatter
from core.formatters.manifestitems_formatter import ManifestitemsFormatter
from core.formatters.navlis_formatter import NavlisFormatter
from core.formatters.spineitemrefs_formatter import SpineitemrefsFormatter


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
        self.creators_formatter: CreatorsFormatter
        self.csslinks_formatter: CsslinksFormatter
        self.languages_formatter: LanguagesFormatter
        self.manifestitems_formatter: ManifestitemsFormatter
        self.navlis_formatter: NavlisFormatter
        self.spineitemrefs_formatter: SpineitemrefsFormatter

        self.creators_formatter = CreatorsFormatter(
            self.package_contents
        )
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

        self.reader: TextReader = Utf8Reader()
        self.writer: TextWriter = Utf8Writer()

        shutil.rmtree(self.dst, ignore_errors=True)

    @abstractmethod
    def build(
        self
    ) -> None:
        pass
