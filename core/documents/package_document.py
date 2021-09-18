from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import BUILD_TIME, Namespace
from core.project import EPUBMetadata, EPUBResource
from core.serialize import write_xml_element


class EPUB3PackageDocument(EPUB3Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(
        self,
        epub_metadata: EPUBMetadata,
        resources: dict[Path, EPUBResource]
    ) -> None:
        self.epub_metadata = epub_metadata
        self.resources = resources

    def epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-doc
        """
        package = make_epub3_package_element(
            self.epub_metadata,
            self.resources,
            self.UNIQUE_IDENTIFIER_ID
        )

        write_xml_element(package, path)


class EPUB2PackageDocument(EPUB2Document):
    """
    An XML document corresponding to the EPUB Package Document.
    """
    pass


def make_epub3_package_element(
    epub_metadata: EPUBMetadata,
    resources: dict[Path, EPUBResource],
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
        UNIQUE_IDENTIFIER_ID
    )
    package.append(metadata)

    manifest = make_epub3_manifest_element(resources)
    package.append(manifest)

    return package


def make_epub3_metadata_element(
    epub_metadata: EPUBMetadata,
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

    dc_date = etree.Element(etree.QName(Namespace.DC.value, "date").text)
    dc_date.text = epub_metadata.date
    metadata.append(dc_date)

    meta_modified = etree.Element(
        "meta",
        attrib={
            "property": "dcterms:modified"
        }
    )
    meta_modified.text = BUILD_TIME
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
