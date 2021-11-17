from pathlib import Path

import pytest

from core.datastructures import Tree
from core.project import Anchor, EPUBMetadata

MODIFIED = "2020-07-19T00:00:00Z"


@pytest.fixture
def epub_metadata_minimal() -> EPUBMetadata:
    epub_metadata = EPUBMetadata("Title")
    epub_metadata.modified = MODIFIED
    return epub_metadata


@pytest.fixture
def nav_trees_empty() -> list[Tree[Anchor]]:
    return []


@pytest.fixture
def nav_trees_nonempty() -> list[Tree[Anchor]]:
    nav_trees: list[Tree[Anchor]] = []
    chapter_1 = Tree(Anchor("Chapter 1", Path("chapter_1.xhtml")), [])
    nav_trees.append(chapter_1)

    chapter_2_1 = Tree(Anchor("Chapter 2.1", Path("chapter_2.xhtml#id-1")), [])
    chapter_2_2 = Tree(Anchor("Chapter 2.2", Path("chapter_2.xhtml#id-2")), [])
    chapter_2 = Tree(
        Anchor("Chapter 2", Path("chapter_2.xhtml")),
        [chapter_2_1, chapter_2_2]
    )
    nav_trees.append(chapter_2)

    chapter_3_1 = Tree(Anchor("Chapter 3.1", Path("chapter_3_1.xhtml")), [])
    chapter_3 = Tree(
        Anchor("Chapter 3", Path("chapter_3.xhtml")),
        [chapter_3_1]
    )
    nav_trees.append(chapter_3)

    return nav_trees
