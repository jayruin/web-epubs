from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from core.documents import NCXDocument

if TYPE_CHECKING:
    from core.datastructures import Tree
    from core.project import Anchor, EPUBMetadata


@pytest.fixture
def ncx_document_empty_nav_trees(
    epub_metadata_minimal: EPUBMetadata
) -> NCXDocument:
    return NCXDocument(
        [],
        epub_metadata_minimal.identifier,
        epub_metadata_minimal.title
    )


@pytest.fixture
def ncx_document_nonempty_nav_trees(
    epub_metadata_minimal: EPUBMetadata,
    nav_trees_nonempty: list[Tree[Anchor]]
) -> NCXDocument:
    return NCXDocument(
        nav_trees_nonempty,
        epub_metadata_minimal.identifier,
        epub_metadata_minimal.title
    )


@pytest.fixture
def expected_file_empty_nav_trees() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "empty_nav_trees.ncx")


@pytest.fixture
def expected_file_nonempty_nav_trees() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "nonempty_nav_trees.ncx")
