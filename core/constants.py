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
    EPUB = "http://www.idpf.org/2007/ops"
    XHTML = "http://www.w3.org/1999/xhtml"


XML_HEADER: str = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
DOCTYPE_HTML_EPUB3: str = "<!DOCTYPE html>"
DOCTYPE_HTML_EPUB2: str = " ".join(
    [
        "<!DOCTYPE html PUBLIC",
        "\"-//W3C//DTD XHTML 1.1//EN\"",
        "\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">"
    ]
)

BUILD_TIME: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
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
