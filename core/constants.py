import datetime
from enum import Enum


INDENT: str = " " * 4

NEWLINE: str = "\n"

# https://html.spec.whatwg.org/#void-elements
HTML_VOID_ELEMENTS: list[str] = [
    "area",
    "base",
    "br",
    "col",
    "embed"
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
]


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

COVER_XHTML: str = "_cover.xhtml"
EPUB_DIRECTORY: str = "./epub"
HTML_DIRECTORY: str = "./html"
METADATA_JSON: str = "_metadata.json"
NAV_JSON: str = "_nav.json"
NAV_XHTML: str = "_nav.xhtml"
PACKAGE_OPF: str = "package.opf"
ROOT_PATH_DIR: str = "OEBPS"
TEMPLATE_XHTML: str = "_template.xhtml"
TOC_NCX: str = "toc.ncx"
TOC_XHTML: str = "_toc.xhtml"

EPUBCHECK_DOWNLOAD_URL: str = (
    "https://api.github.com/repos/w3c/epubcheck/releases/latest"
)
EPUBCHECK_LOCAL_ZIP = "./epubcheck.zip"
EPUBCHECK_ROOT_DIR = "./epubcheck"
EPUBCHECK_SUMMARY_JSON = "./epubcheck.summary.json"

JAVA_EXECUTABLE = "java"
