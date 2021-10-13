import datetime
from enum import Enum


INDENT: str = " " * 4

NEWLINE: str = "\n"


class Encoding(Enum):
    UTF_8 = "UTF-8"
    ASCII = "ASCII"


class Namespace(Enum):
    CONTAINER = "urn:oasis:names:tc:opendocument:xmlns:container"
    DC = "http://purl.org/dc/elements/1.1/"
    EPUB = "http://www.idpf.org/2007/ops"
    NCX = "http://www.daisy.org/z3986/2005/ncx/"
    OPF = "http://www.idpf.org/2007/opf"
    XHTML = "http://www.w3.org/1999/xhtml"


UUID_NAMESPACE = "00000000-0000-0000-0000-000000000000"
BUILD_TIME: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
EPUBCHECK_RELEASES_URL: str = (
    "https://api.github.com/repos/w3c/epubcheck/releases/latest"
)
