from pathlib import Path

from ._copier import Epub2Copier
from core import constants
from core.extendedmimetypes import mimetypes
from core.formatters import Epub2CreatorsFormatter, NavpointsFormatter
from templates.simple._builder import SimpleBuilder


class Epub2Builder(SimpleBuilder):
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
        super(Epub2Builder, self).__init__(src, dst, template_dir)

        template_str = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TEMPLATE_XHTML
            )
        )
        self.html_copier: Epub2Copier = Epub2Copier(
            src=self.src,
            dst=Path(self.dst, constants.ROOT_PATH_DIR).as_posix(),
            template_str=template_str,
            template_indents=2,
            csslinks_formatter=self.csslinks_formatter,
            reader=self.reader,
            writer=self.writer
        )

        self.template_copier: Epub2Copier = Epub2Copier(
            src=self.template_dir,
            dst=self.dst,
            template_str=template_str,
            template_indents=2,
            csslinks_formatter=self.csslinks_formatter,
            reader=self.reader,
            writer=self.writer
        )

        self.epub2_creators_formatter: Epub2CreatorsFormatter
        self.epub2_creators_formatter = Epub2CreatorsFormatter(
            self.package_contents
        )
        self.navpoints_formatter: NavpointsFormatter
        self.navpoints_formatter = NavpointsFormatter(
            self.package_contents
        )

    def _write_toc_ncx(
        self
    ) -> None:
        nav_points = self.navpoints_formatter.run(indents=2)
        content = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TOC_NCX
            )
        )
        content = content.format(
            title=self.package_contents.metadata.title,
            nav=nav_points
        )
        self.writer.write(
            Path(
                self.dst,
                constants.ROOT_PATH_DIR,
                constants.TOC_NCX
            ),
            content
        )

    def _write_toc_xhtml(
        self
    ) -> None:
        nav_lis = self.navlis_formatter.run(indents=3)
        css_links = self.csslinks_formatter.run(
            indents=2,
            target=constants.NAV_XHTML
        )
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
            title=self.package_contents.metadata.title,
            creators=self.epub2_creators_formatter.run(indents=2),
            date=self.package_contents.metadata.date,
            cover_file=self.package_contents.metadata.cover,
            cover_media_type=mimetypes.guess_type(
                self.package_contents.metadata.cover
            )[0],
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

    def build(
        self
    ) -> None:
        self._write_contents_from_template()
        self._write_toc_ncx()
        self._write_toc_xhtml()
        self._write_cover_xhtml()
        self._write_package_opf()
        self._create_default_cover_if_needed()
