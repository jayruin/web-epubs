from pathlib import Path

from lxml import etree

from .epub2document import EPUB2Document
from .epub3document import EPUB3Document
from core.constants import Namespace
from core.serialize import write_xml_element


class ContainerXML(EPUB3Document, EPUB2Document):
    """
    An XML document corresponding to the container.xml file.
    """
    def __init__(self, package_document: Path) -> None:
        self.package_document = package_document

    def epub3(self, path: Path) -> None:
        """
        https://www.w3.org/publishing/epub3/epub-ocf.html#sec-container-metainf-container.xml
        """
        container = make_container_element(self.package_document)

        write_xml_element(container, path)

    def epub2(self, path: Path) -> None:
        """
        http://www.idpf.org/doc_library/epub/OCF_2.0.1_draft.doc Section 3.5.1
        """
        self.epub3(path)


def make_container_element(package_document: Path) -> etree._Element:
    container = etree.Element(
        "container",
        attrib={"version": "1.0"},
        nsmap={None: Namespace.CONTAINER.value}
    )

    rootfiles = etree.Element("rootfiles")
    container.append(rootfiles)

    rootfile = etree.Element(
        "rootfile",
        attrib={
            "full-path": package_document.as_posix(),
            "media-type": "application/oebps-package+xml"
        }
    )
    rootfiles.append(rootfile)

    return container
