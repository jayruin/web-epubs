from __future__ import annotations
from typing import TYPE_CHECKING

from lxml import etree

from core.constants import Namespace

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional

    from core.project import EPUBMetadata, EPUBResource


def make_package_element(
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

    metadata = make_metadata_element(
        epub_metadata,
        pre_paginated,
        UNIQUE_IDENTIFIER_ID
    )
    package.append(metadata)

    manifest = make_manifest_element(resources)
    package.append(manifest)

    spine = make_spine_element(
        resources,
        progression,
        page_progression_direction
    )
    package.append(spine)

    return package


def make_metadata_element(
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


def make_manifest_element(
    resources: dict[Path, EPUBResource]
) -> etree._Element:
    manifest = etree.Element("manifest")

    if len(resources) == 0:
        manifest.text = ""

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


def make_spine_element(
    resources: dict[Path, EPUBResource],
    progression: list[Path],
    page_progression_direction: Optional[str]
) -> etree._Element:
    spine = etree.Element("spine")

    if len(progression) == 0:
        spine.text = ""

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
