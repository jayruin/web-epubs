from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import Namespace
from core.serialize import write_xml_element


class ContainerXML(EPUB3Document, EPUB2Document):
    """
    https://www.w3.org/publishing/epub3/epub-ocf.html#sec-container-metainf-container.xml
    An XML document corresponding to the container.xml file.
    """
    def __init__(self, package_document: Path) -> None:
        self.package_document = package_document

    def epub3(self, path: Path) -> None:
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
                "full-path": self.package_document.as_posix(),
                "media-type": "application/oebps-package+xml"
            }
        )
        rootfiles.append(rootfile)

        write_xml_element(container, path)

    def epub2(self, path: Path) -> None:
        self.epub3(path)
