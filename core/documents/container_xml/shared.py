from pathlib import Path

from lxml import etree

from core.constants import Namespace


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
