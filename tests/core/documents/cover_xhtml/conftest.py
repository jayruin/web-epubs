from pathlib import Path

import pytest

from core.documents import CoverXHTML


@pytest.fixture
def cover_xhtml_no_sep() -> CoverXHTML:
    cover_file = Path("cover.jpg")
    return CoverXHTML(cover_file)


@pytest.fixture
def cover_xhtml_sep() -> CoverXHTML:
    cover_file = Path("img", "cover.jpg")
    return CoverXHTML(cover_file)


@pytest.fixture
def expected_file_epub3_no_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub3_no_sep.xhtml")


@pytest.fixture
def expected_file_epub3_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub3_sep.xhtml")


@pytest.fixture
def expected_file_epub2_no_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub2_no_sep.xhtml")


@pytest.fixture
def expected_file_epub2_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub2_sep.xhtml")
