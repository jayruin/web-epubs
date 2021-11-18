from pathlib import Path
from typing import Optional

from lxml import etree

from .abcs import EPUB3Document, EPUB2Document
from core.constants import Namespace
from core.project import EPUBMetadata, EPUBResource, TypedAnchor
from core.serialize import write_xml_element


class EPUB3PackageDocument(EPUB3Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(
        self,
        epub_metadata: EPUBMetadata,
        resources: dict[Path, EPUBResource],
        progression: list[Path],
        pre_paginated: bool
    ) -> None:
        self.epub_metadata = epub_metadata
        self.resources = resources
        self.progression = progression
        self.pre_paginated = pre_paginated

    def write_epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-doc
        """
        package = make_epub3_package_element(
            self.epub_metadata,
            self.resources,
            self.progression,
            self.pre_paginated,
            self.epub_metadata.direction,
            self.UNIQUE_IDENTIFIER_ID
        )

        write_xml_element(package, path)


class EPUB2PackageDocument(EPUB2Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(
        self,
        epub_metadata: EPUBMetadata,
        resources: dict[Path, EPUBResource],
        progression: list[Path],
        toc: Path,
        landmarks: Optional[list[TypedAnchor]] = None
    ) -> None:
        self.epub_metadata = epub_metadata
        self.resources = resources
        self.progression = progression
        self.toc = toc
        self.landmarks = landmarks

    def write_epub2(self, path: Path) -> None:
        """
        http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.0
        """
        package = make_epub2_package_element(
            self.epub_metadata,
            self.resources,
            self.progression,
            self.toc,
            self.landmarks,
            self.UNIQUE_IDENTIFIER_ID
        )

        write_xml_element(package, path)


def make_epub3_package_element(
    epub_metadata: EPUBMetadata,
    resources: dict[Path, EPUBResource],
    progression: list[Path],
    pre_paginated: bool,
    page_progression_direction: Optional[str],
    UNIQUE_IDENTIFIER_ID: str
) -> etree._Element:
    package = etree.Element(
        "package",
        attrib={
            "unique-identifier": UNIQUE_IDENTIFIER_ID,
            "version": "3.0"
        },
        nsmap={
            None: Namespace.OPF.value
        }
    )

    metadata = make_epub3_metadata_element(
        epub_metadata,
        pre_paginated,
        UNIQUE_IDENTIFIER_ID
    )
    package.append(metadata)

    manifest = make_epub3_manifest_element(resources)
    package.append(manifest)

    spine = make_epub3_spine_element(
        resources,
        progression,
        page_progression_direction
    )
    package.append(spine)

    return package


def make_epub3_metadata_element(
    epub_metadata: EPUBMetadata,
    pre_paginated: bool,
    UNIQUE_IDENTIFIER_ID: str
) -> etree._Element:
    metadata = etree.Element(
        "metadata",
        nsmap={
            "dc": Namespace.DC.value
        }
    )

    dc_identifier = etree.Element(
        etree.QName(Namespace.DC.value, "identifier").text,
        attrib={
            "id": UNIQUE_IDENTIFIER_ID
        }
    )
    dc_identifier.text = epub_metadata.identifier
    metadata.append(dc_identifier)

    for language in epub_metadata.languages:
        dc_language = etree.Element(
            etree.QName(Namespace.DC.value, "language").text
        )
        dc_language.text = language
        metadata.append(dc_language)

    dc_title = etree.Element(
        etree.QName(Namespace.DC.value, "title").text,
        attrib={
            "id": "title-id"
        }
    )
    dc_title.text = epub_metadata.title
    metadata.append(dc_title)
    dc_title_meta = etree.Element(
        "meta",
        attrib={
            "refines": "#title-id",
            "property": "title-type"
        }
    )
    dc_title_meta.text = "main"
    metadata.append(dc_title_meta)

    for id_counter, creator in enumerate(epub_metadata.creators, start=1):
        roles = epub_metadata.creators[creator]
        dc_creator = etree.Element(
            etree.QName(Namespace.DC.value, "creator").text,
            attrib={
                "id": f"creator-id-{id_counter}"
            }
        )
        dc_creator.text = creator
        metadata.append(dc_creator)
        for role in roles:
            dc_creator_meta = etree.Element(
                "meta",
                attrib={
                    "refines": f"#creator-id-{id_counter}",
                    "property": "role",
                    "scheme": "marc:relators"
                }
            )
            dc_creator_meta.text = role
            metadata.append(dc_creator_meta)

    if epub_metadata.date:
        dc_date = etree.Element(etree.QName(Namespace.DC.value, "date").text)
        dc_date.text = epub_metadata.date
        metadata.append(dc_date)

    if pre_paginated:
        pre_paginated_meta = etree.Element(
            "meta",
            attrib={
                "property": "rendition:layout"
            }
        )
        pre_paginated_meta.text = "pre-paginated"
        metadata.append(pre_paginated_meta)

    meta_modified = etree.Element(
        "meta",
        attrib={
            "property": "dcterms:modified"
        }
    )
    meta_modified.text = epub_metadata.modified
    metadata.append(meta_modified)

    return metadata


def make_epub3_manifest_element(
    resources: dict[Path, EPUBResource]
) -> etree._Element:
    manifest = etree.Element("manifest")

    for path in sorted(resources, key=lambda p: p.as_posix()):
        epub_resource = resources[path]
        item = etree.Element(
            "item",
            attrib={
                "href": epub_resource.href.as_posix(),
                "id": epub_resource.manifest_id,
                "media-type": epub_resource.mimetype
            }
        )
        if epub_resource.properties:
            item.set("properties", epub_resource.properties)
        manifest.append(item)

    return manifest


def make_epub3_spine_element(
    resources: dict[Path, EPUBResource],
    progression: list[Path],
    page_progression_direction: Optional[str]
) -> etree._Element:
    spine = etree.Element("spine")

    for path in progression:
        itemref = etree.Element(
            "itemref",
            attrib={
                "idref": resources[path].manifest_id,
                "linear": "yes"
            }
        )
        spine.append(itemref)

    if page_progression_direction is not None:
        spine.set("page-progression-direction", page_progression_direction)

    return spine


def make_epub2_package_element(
    epub_metadata: EPUBMetadata,
    resources: dict[Path, EPUBResource],
    progression: list[Path],
    toc: Path,
    landmarks: Optional[list[TypedAnchor]],
    UNIQUE_IDENTIFIER_ID: str
) -> etree._Element:
    package = etree.Element(
        "package",
        attrib={
            "unique-identifier": UNIQUE_IDENTIFIER_ID,
            "version": "2.0"
        },
        nsmap={
            None: Namespace.OPF.value
        }
    )

    metadata = make_epub2_metadata_element(
        epub_metadata,
        resources,
        UNIQUE_IDENTIFIER_ID
    )
    package.append(metadata)

    manifest = make_epub2_manifest_element(resources)
    package.append(manifest)

    spine = make_epub2_spine_element(resources, progression, toc)
    package.append(spine)

    if landmarks is not None:
        guide = make_epub2_guide_element(landmarks)
        package.append(guide)

    return package


def make_epub2_metadata_element(
    epub_metadata: EPUBMetadata,
    resources: dict[Path, EPUBResource],
    UNIQUE_IDENTIFIER_ID: str
) -> etree._Element:
    metadata = etree.Element(
        "metadata",
        nsmap={
            "dc": Namespace.DC.value,
            "opf": Namespace.OPF.value
        }
    )

    dc_identifier = etree.Element(
        etree.QName(Namespace.DC.value, "identifier").text,
        attrib={
            "id": UNIQUE_IDENTIFIER_ID
        }
    )
    dc_identifier.text = epub_metadata.identifier
    metadata.append(dc_identifier)

    for language in epub_metadata.languages:
        dc_language = etree.Element(
            etree.QName(Namespace.DC.value, "language").text
        )
        dc_language.text = language
        metadata.append(dc_language)

    dc_title = etree.Element(
        etree.QName(Namespace.DC.value, "title").text
    )
    dc_title.text = epub_metadata.title
    metadata.append(dc_title)

    for creator, roles in epub_metadata.creators.items():
        for role in roles:
            dc_creator = etree.Element(
                etree.QName(Namespace.DC.value, "creator").text,
                attrib={
                    etree.QName(Namespace.OPF.value, "role"): role
                }
            )
            dc_creator.text = creator
            metadata.append(dc_creator)

    if epub_metadata.date:
        dc_date = etree.Element(etree.QName(Namespace.DC.value, "date").text)
        dc_date.text = epub_metadata.date
        metadata.append(dc_date)

    if epub_metadata.cover:
        meta_cover = etree.Element(
            "meta",
            attrib={
                "name": "cover",
                "content": resources[epub_metadata.cover].manifest_id
            }
        )
        metadata.append(meta_cover)

    return metadata


def make_epub2_manifest_element(
    resources: dict[Path, EPUBResource]
) -> etree._Element:
    manifest = etree.Element("manifest")

    for path in sorted(resources, key=lambda p: p.as_posix()):
        epub_resource = resources[path]
        item = etree.Element(
            "item",
            attrib={
                "href": epub_resource.href.as_posix(),
                "id": epub_resource.manifest_id,
                "media-type": epub_resource.mimetype
            }
        )
        manifest.append(item)

    return manifest


def make_epub2_spine_element(
    resources: dict[Path, EPUBResource],
    progression: list[Path],
    toc: Path
) -> etree._Element:
    spine = etree.Element(
        "spine",
        attrib={
            "toc": resources[toc].manifest_id
        }
    )

    for path in progression:
        itemref = etree.Element(
            "itemref",
            attrib={
                "idref": resources[path].manifest_id,
                "linear": "yes"
            }
        )
        spine.append(itemref)

    return spine


def make_epub2_guide_element(landmarks: list[TypedAnchor]) -> etree._Element:
    guide = etree.Element("guide")

    for anchor in landmarks:
        assert anchor.type
        reference = etree.Element(
            "reference",
            attrib={
                "type": anchor.type,
                "title": anchor.text,
                "href": anchor.href.as_posix()
            }
        )
        guide.append(reference)

    return guide
