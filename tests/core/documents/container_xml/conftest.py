from pathlib import Path

import pytest

from core.documents import ContainerXML


@pytest.fixture
def container_xml_no_sep() -> ContainerXML:
    package_document = Path("package.opf")
    return ContainerXML(package_document)


@pytest.fixture
def container_xml_sep() -> ContainerXML:
    package_document = Path("OEBPS/package.opf")
    return ContainerXML(package_document)


@pytest.fixture
def expected_file_no_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "no_sep.xml")


@pytest.fixture
def expected_file_sep() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "sep.xml")
