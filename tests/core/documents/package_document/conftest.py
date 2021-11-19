from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from core.documents import EPUB3PackageDocument

if TYPE_CHECKING:
    from core.project import EPUBMetadata, EPUBResource


@pytest.fixture
def epub3_package_document_minimal(
    epub_metadata_minimal: EPUBMetadata
) -> EPUB3PackageDocument:
    return EPUB3PackageDocument(epub_metadata_minimal, {}, [], False)


@pytest.fixture
def epub3_package_document_maximal(
    epub_metadata_maximal: EPUBMetadata,
    resources_nonempty: dict[Path, EPUBResource],
    progression_nonempty: list[Path]
) -> EPUB3PackageDocument:
    return EPUB3PackageDocument(
        epub_metadata_maximal,
        resources_nonempty,
        progression_nonempty,
        True
    )


@pytest.fixture
def expected_file_epub3_minimal() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub3_package_document_minimal.xhtml"
    )


@pytest.fixture
def expected_file_epub3_maximal() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub3_package_document_maximal.xhtml"
    )
