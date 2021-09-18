from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import BUILD_TIME, Namespace
from core.project import Metadata
from core.serialize import write_xml_element


class PackageDocument(EPUB3Document, EPUB2Document):
    """
    https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-doc
    An XML document corresponding to the EPUB Package Document.
    """
    UNIQUE_IDENTIFIER_ID = "publication-id"

    def __init__(self, metadata: Metadata) -> None:
        self.metadata = metadata

    def epub3(self, path: Path) -> None:
        package = etree.Element(
            "package",
            attrib={
                "unique-identifier": self.UNIQUE_IDENTIFIER_ID,
                "version": "3.0"
            },
            nsmap={
                None: Namespace.OPF.value
            }
        )

        metadata = self.epub3_generate_metadata_element()
        package.append(metadata)

        write_xml_element(package, path)

    def epub3_generate_metadata_element(self) -> etree._Element:
        metadata = etree.Element(
            "metadata",
            nsmap={
                "dc": Namespace.DC.value
            }
        )

        dc_identifier = etree.Element(
            etree.QName(Namespace.DC.value, "identifier").text,
            attrib={
                "id": self.UNIQUE_IDENTIFIER_ID
            }
        )
        dc_identifier.text = self.metadata.identifier
        metadata.append(dc_identifier)

        for language in self.metadata.languages:
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
        dc_title.text = self.metadata.title
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

        for id_counter, creator in enumerate(self.metadata.creators, start=1):
            roles = self.metadata.creators[creator]
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
        dc_date.text = self.metadata.date
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

    def epub2(self, path: Path) -> None: ...
