from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import Namespace
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

        return metadata

    def epub2(self, path: Path) -> None: ...
