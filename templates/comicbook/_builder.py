from pathlib import Path

from ._copier import ComicbookCopier
from core import constants
from templates.simple._builder import SimpleBuilder


class ComicbookBuilder(SimpleBuilder):
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
        super(ComicbookBuilder, self).__init__(src, dst, template_dir)

        template_str = self.reader.read(
            Path(
                self.template_dir,
                constants.ROOT_PATH_DIR,
                constants.TEMPLATE_XHTML
            )
        )
        self.html_copier: ComicbookCopier = ComicbookCopier(
            src=self.src,
            dst=Path(self.dst, constants.ROOT_PATH_DIR).as_posix(),
            template_str=template_str,
            template_indents=3,
            csslinks_formatter=self.csslinks_formatter,
            reader=self.reader,
            writer=self.writer
        )

        self.template_copier: ComicbookCopier = ComicbookCopier(
            src=self.template_dir,
            dst=self.dst,
            template_str=template_str,
            template_indents=3,
            csslinks_formatter=self.csslinks_formatter,
            reader=self.reader,
            writer=self.writer
        )
