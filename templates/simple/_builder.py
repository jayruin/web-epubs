from pathlib import Path

from ._copier import SimpleCopier
from core import constants
from core.cover import fill_blank_cover
from core.extendedmimetypes import mimetypes
from core.packaging import PackageBuilder


class SimpleBuilder(PackageBuilder):
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
        super(SimpleBuilder, self).__init__(src, dst, template_dir)

        template_str = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TEMPLATE_XHTML
            )
        )
        self.html_copier: SimpleCopier = SimpleCopier(
            src=self.src,
            dst=str(Path(self.dst, constants.ROOT_PATH_DIR)),
            template_str=template_str,
            template_indents=3,
            csslinks_formatter=self.csslinks_formatter
        )

        self.template_copier: SimpleCopier = SimpleCopier(
            src=self.template_dir,
            dst=self.dst,
            template_str=template_str,
            template_indents=3,
            csslinks_formatter=self.csslinks_formatter
        )

    def _write_contents_from_template(
        self
    ) -> None:
        self.template_copier.copy_over()
        self.html_copier.copy_over()

    def _write_nav_toc_xhtml(
        self
    ) -> None:
        nav_lis = self.navlis_formatter.run(indents=5)
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
            cover_file=self.package_contents.metadata.cover,
            css=self.csslinks_formatter.run(
                indents=2,
                target=constants.COVER_XHTML
            )
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
            title=self.package_contents.metadata.title,
            author=self.package_contents.metadata.author,
            date=self.package_contents.metadata.date,
            modified=constants.BUILD_TIME,
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

    def _create_default_cover_if_needed(
        self
    ) -> None:
        cover_path = Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            self.package_contents.metadata.cover
        )

        fill_blank_cover(cover_path)

    def build(
        self
    ) -> None:
        self._write_contents_from_template()
        self._write_nav_toc_xhtml()
        self._write_cover_xhtml()
        self._write_package_opf()
        self._create_default_cover_if_needed()
