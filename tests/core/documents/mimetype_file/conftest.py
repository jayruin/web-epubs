from pathlib import Path

import pytest

from core.documents import MimetypeFile


@pytest.fixture
def mimetype_file() -> MimetypeFile:
    return MimetypeFile()


@pytest.fixture
def expected_file() -> Path:
    parent_directory = Path(__file__).parent
    return Path(parent_directory, "expected", "mimetype")
