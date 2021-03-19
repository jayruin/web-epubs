import datetime


INDENT: str = " " * 4

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
