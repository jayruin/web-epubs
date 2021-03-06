from .base_build_job import BaseBuildJob
from .epub_type import EPUBType
from .epub_version import EPUBVersion


class EPUB2BuildJob(BaseBuildJob):
    @classmethod
    @property
    def epub_type(cls) -> EPUBType:
        return EPUBType.EPUB2

    @classmethod
    @property
    def epub_version(cls) -> EPUBVersion:
        return EPUBVersion.EPUB2

    def run(self) -> None:
        self._clear()
        self._write_mimetype_file()
        self._fill_meta_inf()
        self._import_resources()
        self._convert_html()
        self._write_cover()
        self._write_navigation_document()
        self._write_ncx_document()
        self._write_package_document()
