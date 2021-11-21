from pathlib import Path
from typing import Optional

from lxml import etree

from core.constants import Namespace
from core.project import EPUBMetadata, EPUBResource, TypedAnchor


def make_package_element(
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

    metadata = make_metadata_element(
        epub_metadata,
        resources,
        UNIQUE_IDENTIFIER_ID
    )
    package.append(metadata)

    manifest = make_manifest_element(resources)
    package.append(manifest)

    spine = make_spine_element(resources, progression, toc)
    package.append(spine)

    if landmarks:
        guide = make_guide_element(landmarks)
        package.append(guide)

    return package


def make_metadata_element(
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


def make_manifest_element(
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


def make_spine_element(
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


def make_guide_element(landmarks: list[TypedAnchor]) -> etree._Element:
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
