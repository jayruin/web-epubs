from pathlib import Path

from lxml import etree

from .epub3document import EPUB3Document
from .epub2document import EPUB2Document
from core.constants import Encoding, INDENT, Namespace, XML_HEADER


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

        etree.indent(container, space=INDENT)
        with open(path, "wb") as f:
            f.write(
                etree.tostring(
                    container,
                    encoding=Encoding.UTF_8.value,
                    doctype=XML_HEADER
                )
            )

    def epub2(self, path: Path) -> None:
        self.epub3(path)
