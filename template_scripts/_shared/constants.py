import datetime
from typing import List


INDENT: str = " " * 4
BUILD_TIME: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
COVER_XHTML: str = "_cover.xhtml"
FILES_TO_OVERWRITE: List[str] = ["img/cover.jpg"]
METADATA_JSON: str = "_metadata.json"
NAV_JSON: str = "_nav.json"
NAV_XHTML: str = "_nav.xhtml"
PACKAGE_OPF: str = "package.opf"
ROOT_PATH_DIR: str = "OEBPS"
TEMPLATE_XHTML: str = "_template.xhtml"
TOC_XHTML: str = "_toc.xhtml"
