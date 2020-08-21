import json
import mimetypes
from pathlib import Path
import shutil
from typing import List, Type

from core import constants
from core.files.readers import TextReader, Utf8Reader
from core.files.writers import TextWriter, Utf8Writer
from core.formatters import (
    CsslinksFormatter,
    LanguagesFormatter,
    ManifestitemsFormatter,
    NavlisFormatter,
    SpineitemrefsFormatter
)
from core.config.metadata import Metadata
from core.config.nav_node import NavNode
from core.package_contents import PackageContents
from template_scripts._shared.cover import create_default_cover
from template_scripts._shared.package_copier import PackageCopier


class Builder:
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
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

        self.src: str = src
        self.dst: str = dst
        self.template_dir: str = template_dir

        self.metadata: Metadata = Metadata.from_json_path(
            Path(
                self.src,
                constants.METADATA_JSON
            )
        )

        shutil.rmtree(self.dst, ignore_errors=True)

        template_str = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TEMPLATE_XHTML
            )
        )
        self.html_copier: PackageCopier = PackageCopier(
            src=self.src,
            dst=str(Path(self.dst, constants.ROOT_PATH_DIR)),
            template_str=template_str,
            template_indents=3
        )

        self.template_copier: PackageCopier = PackageCopier(
            src=self.template_dir,
            dst=self.dst,
            template_str=template_str,
            template_indents=3
        )

        content = self.reader.read(
            Path(
                self.src,
                constants.NAV_JSON
            )
        )
        self.nav_nodes: List[NavNode] = [
            NavNode.from_dict(d)
            for d in json.loads(content)
        ]

    def _write_contents_from_template(
        self
    ) -> None:
        css_links = self.csslinks_formatter.run(indents=2)
        self.template_copier.copy_over(css_links)
        self.html_copier.copy_over(css_links)

    def _write_nav_toc_xhtml(
        self
    ) -> None:
        nav_lis = self.navlis_formatter.run(indents=5)
        css_links = self.csslinks_formatter.run(indents=2)
        content = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TOC_XHTML
            )
        )
        content = content.format(
            nav=nav_lis,
            css=css_links
        )
        self.writer.write(
            Path(
                self.dst,
                constants.ROOT_PATH_DIR,
                constants.TOC_XHTML
            ),
            content
        )
        content = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.NAV_XHTML
            )
        )
        content = content.format(
            nav=nav_lis,
            css=css_links
        )
        self.writer.write(
            Path(
                self.dst,
                constants.ROOT_PATH_DIR,
                constants.NAV_XHTML
            ),
            content
        )

    def _write_cover_xhtml(
        self
    ) -> None:
        cover_src = Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.COVER_XHTML
        )
        cover_dst = Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            constants.COVER_XHTML
        )
        content = self.reader.read(cover_src)
        content = content.format(
            cover_file=self.metadata.cover,
            css=self.csslinks_formatter.run(indents=2)
        )
        self.writer.write(cover_dst, content)

    def _write_package_opf(
        self
    ) -> None:
        content = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.PACKAGE_OPF
            )
        )
        content = content.format(
            languages=self.languages_formatter.run(indents=2),
            title=self.metadata.title,
            author=self.metadata.author,
            date=self.metadata.date,
            modified=constants.BUILD_TIME,
            cover_file=self.metadata.cover,
            cover_media_type=mimetypes.guess_type(self.metadata.cover)[0],
            manifest=self.manifestitems_formatter.run(indents=2),
            spine=self.spineitemrefs_formatter.run(indents=2)
        )
        self.writer.write(
            Path(
                self.dst,
                constants.ROOT_PATH_DIR,
                constants.PACKAGE_OPF
            ),
            content
        )

    def _create_default_cover_if_needed(
        self
    ) -> None:
        cover_path = Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            self.metadata.cover
        )

        if not cover_path.exists():
            create_default_cover(cover_path)

    def build(
        self
    ) -> None:
        self._write_contents_from_template()
        self._write_nav_toc_xhtml()
        self._write_cover_xhtml()
        self._write_package_opf()
        self._create_default_cover_if_needed()
