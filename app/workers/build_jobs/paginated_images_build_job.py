from collections import defaultdict
from pathlib import Path

from .base_build_job import BaseBuildJob
from .epub_type import EPUBType
from .epub_version import EPUBVersion
from core.documents import PaginatedImage
from core.extendedmimetypes import mimetypes
from core.project import EPUBResource


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
        self._clear()
        self._write_mimetype_file()
        self._fill_meta_inf()
        self._import_resources()
        self._write_cover(add_to_spine=False)
        self._write_navigation_document(add_to_spine=False)
        self._paginate()
        self._write_package_document(pre_paginated=True)

    def _paginate(self) -> None:
        parent_to_paginated_images: dict[Path, list[Path]] = defaultdict(list)
        for path in self._resource_manager.resources:
            image_path = Path(self._resource_manager.root, path)
            if self.is_page(image_path):
                document = PaginatedImage(image_path)
                relative_document_path = path.with_suffix(".xhtml")
                document_path = image_path.with_suffix(".xhtml")
                document.epub3(document_path)
                parent_to_paginated_images[
                    relative_document_path.parent
                ].append(
                    relative_document_path
                )
        for paginated_images in parent_to_paginated_images.values():
            paginated_images.sort(key=lambda path: int(path.stem))
            if len(paginated_images) > 0:
                paginated_image_index = self._progression.index(
                    paginated_images[0]
                )
                self._progression = [
                    *self._progression[:paginated_image_index],
                    *paginated_images,
                    *self._progression[paginated_image_index + 1:]
                ]
            for paginated_image in paginated_images:
                self._resource_manager.resources[
                    paginated_image
                ] = EPUBResource(
                    paginated_image
                )

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
