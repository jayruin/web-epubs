from .base_build_job import BaseBuildJob
from .epub_type import EPUBType
from .epub_version import EPUBVersion


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
