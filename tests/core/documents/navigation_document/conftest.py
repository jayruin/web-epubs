from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from core.documents import NavigationDocument

if TYPE_CHECKING:
    from core.datastructures import Tree
    from core.project import Anchor, TypedAnchor


@pytest.fixture
def navigation_document_no_landmarks(
    nav_trees_nonempty: list[Tree[Anchor]]
) -> NavigationDocument:
    return NavigationDocument(nav_trees_nonempty, None)


@pytest.fixture
def navigation_document_empty_landmarks(
    nav_trees_nonempty: list[Tree[Anchor]]
) -> NavigationDocument:
    return NavigationDocument(nav_trees_nonempty, [])


@pytest.fixture
def navigation_document_nonempty_landmarks(
    nav_trees_nonempty: list[Tree[Anchor]],
    landmarks_nonempty: list[TypedAnchor]
) -> NavigationDocument:
    return NavigationDocument(nav_trees_nonempty, landmarks_nonempty)


@pytest.fixture
def expected_file_epub3_no_landmarks() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub3_no_landmarks.xhtml")


@pytest.fixture
def expected_file_epub3_nonempty_landmarks() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub3_nonempty_landmarks.xhtml")


@pytest.fixture
def expected_file_epub2_no_landmarks() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "epub2_no_landmarks.xhtml")
