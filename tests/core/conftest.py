from pathlib import Path

import pytest

from core.datastructures import Tree
from core.project import Anchor, EPUBMetadata, EPUBResource, TypedAnchor

MODIFIED = "2020-07-19T00:00:00Z"


@pytest.fixture
def epub_metadata_minimal() -> EPUBMetadata:
    epub_metadata = EPUBMetadata("Title", modified=MODIFIED)
    return epub_metadata


@pytest.fixture
def epub_metadata_maximal() -> EPUBMetadata:
    epub_metadata = EPUBMetadata(
        "Title",
        creators={
            "Creator No Roles": [],
            "Creator One Role": ["aut"],
            "Creator Two Roles": ["ill"]
        },
        languages=["en", "es"],
        cover=Path("img/cover.jpg"),
        direction="rtl",
        date=MODIFIED,
        identifier="urn:uuid:00000000-0000-0000-0000-000000000000",
        modified=MODIFIED
    )
    return epub_metadata


@pytest.fixture
def nav_trees_nonempty() -> list[Tree[Anchor]]:
    nav_trees: list[Tree[Anchor]] = []

    cover = Tree(Anchor("Cover", Path("_cover.xhtml")), [])
    nav_trees.append(cover)

    nav = Tree(Anchor("Table of Contents", Path("_nav.xhtml")), [])
    nav_trees.append(nav)

    chapter_1 = Tree(Anchor("Chapter 1", Path("chapter_1.xhtml")), [])
    nav_trees.append(chapter_1)

    chapter_2_1 = Tree(Anchor("Chapter 2.1", Path("chapter_2.xhtml#id-1")), [])
    chapter_2_2 = Tree(Anchor("Chapter 2.2", Path("chapter_2.xhtml#id-2")), [])
    chapter_2 = Tree(
        Anchor("Chapter 2", Path("chapter_2.xhtml")),
        [chapter_2_1, chapter_2_2]
    )
    nav_trees.append(chapter_2)

    chapter_3_1 = Tree(Anchor("Chapter 3.1", Path("chapter_3", "1.xhtml")), [])
    chapter_3 = Tree(
        Anchor("Chapter 3", Path("chapter_3.xhtml")),
        [chapter_3_1]
    )
    nav_trees.append(chapter_3)

    return nav_trees


@pytest.fixture
def landmarks_nonempty() -> list[TypedAnchor]:
    landmarks: list[TypedAnchor] = []

    cover = TypedAnchor("Cover", Path("_cover.xhtml"), "cover")
    landmarks.append(cover)

    nav = TypedAnchor("Table of Contents", Path("_nav.xhtml"), "toc")
    landmarks.append(nav)

    bodymatter = TypedAnchor(
        "Begin Reading",
        Path("chapter_1.xhtml"),
        "bodymatter"
    )
    landmarks.append(bodymatter)

    return landmarks


@pytest.fixture
def resources_nonempty() -> dict[Path, EPUBResource]:
    resources: dict[Path, EPUBResource] = {}

    path = Path("cover.jpg")
    resource = EPUBResource(path, manifest_properties={"cover-image"})
    resources[path] = resource

    path = Path("_cover.xhtml")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("_nav.xhtml")
    resource = EPUBResource(path, manifest_properties={"nav"})
    resources[path] = resource

    path = Path("css/style.css")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("js/script.js")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("chapter_1.xhtml")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("chapter_2.xhtml")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("chapter_3.xhtml")
    resource = EPUBResource(path)
    resources[path] = resource

    path = Path("chapter_3", "1.xhtml")
    resource = EPUBResource(path, manifest_properties={"scripted"})
    resources[path] = resource

    for count, resource in enumerate(resources.values()):
        resource.id_count = count

    return resources


@pytest.fixture
def resources_nonempty_ncx(
    resources_nonempty: dict[Path, EPUBResource]
) -> dict[Path, EPUBResource]:
    path = Path("_toc.ncx")
    resource = EPUBResource(path)
    resource.id_count = len(resources_nonempty)
    resources_nonempty[path] = resource
    return resources_nonempty


@pytest.fixture
def progression_nonempty() -> list[Path]:
    return [
        Path("_cover.xhtml"),
        Path("_nav.xhtml"),
        Path("chapter_1.xhtml"),
        Path("chapter_2.xhtml"),
        Path("chapter_3.xhtml"),
        Path("chapter_3", "1.xhtml")
    ]
