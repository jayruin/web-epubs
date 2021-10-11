from pathlib import Path

from .base_build_job import BaseBuildJob
from .epub_type import EPUBType
from .epub_version import EPUBVersion
from core.extendedmimetypes import mimetypes


class PaginatedImagesBuildJob(BaseBuildJob):
    FORMATS = {"image/jpeg", "image/png"}

    @classmethod
    @property
    def epub_type(cls) -> EPUBType:
        return EPUBType.PAGINATED_IMAGES

    @classmethod
    @property
    def epub_version(cls) -> EPUBVersion:
        return EPUBVersion.EPUB3

    def run(self) -> None:
        raise NotImplementedError

    @classmethod
    def is_page(cls, path: Path) -> bool:
        if not path.is_file():
            return False
        if mimetypes.guess_type(path)[0] not in cls.FORMATS:
            return False
        try:
            page_number = int(path.stem)
            return page_number > 0
        except ValueError:
            return False
