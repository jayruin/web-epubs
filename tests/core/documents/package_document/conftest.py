from pathlib import Path

import pytest

from core.documents import EPUB3PackageDocument, EPUB2PackageDocument
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
def epub2_package_document_no_landmarks(
    epub_metadata_minimal: EPUBMetadata,
    resources_nonempty_ncx: dict[Path, EPUBResource],
    progression_nonempty: list[Path]
) -> EPUB2PackageDocument:
    return EPUB2PackageDocument(
        epub_metadata_minimal,
        resources_nonempty_ncx,
        progression_nonempty,
        Path("_toc.ncx")
    )


@pytest.fixture
def epub2_package_document_empty_landmarks(
    epub_metadata_minimal: EPUBMetadata,
    resources_nonempty_ncx: dict[Path, EPUBResource],
    progression_nonempty: list[Path]
) -> EPUB2PackageDocument:
    return EPUB2PackageDocument(
        epub_metadata_minimal,
        resources_nonempty_ncx,
        progression_nonempty,
        Path("_toc.ncx"),
        []
    )


@pytest.fixture
def epub2_package_document_nonempty_landmarks(
    epub_metadata_minimal: EPUBMetadata,
    resources_nonempty_ncx: dict[Path, EPUBResource],
    progression_nonempty: list[Path],
    landmarks_nonempty
) -> EPUB2PackageDocument:
    return EPUB2PackageDocument(
        epub_metadata_minimal,
        resources_nonempty_ncx,
        progression_nonempty,
        Path("_toc.ncx"),
        landmarks_nonempty
    )


@pytest.fixture
def expected_file_epub3_minimal() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub3_package_document_minimal.opf"
    )


@pytest.fixture
def expected_file_epub3_maximal() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub3_package_document_maximal.opf"
    )


@pytest.fixture
def expected_file_epub2_no_landmarks() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub2_package_document_no_landmarks.opf"
    )


@pytest.fixture
def expected_file_epub2_nonempty_landmarks() -> Path:
    parent_directory = Path(__file__).parent
    return Path(
        parent_directory,
        "expected",
        "epub2_package_document_nonempty_landmarks.opf"
    )
