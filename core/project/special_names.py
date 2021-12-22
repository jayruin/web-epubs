from dataclasses import dataclass


@dataclass(frozen=True)
class SpecialNames:
    mimetype_file: str = "mimetype"
    # META-INF
    meta_inf: str = "META-INF"
    container_xml: str = "container.xml"
    # Resources
    resources_directory: str = "OEBPS"
    package_document: str = "_package.opf"
    cover_xhtml: str = "_cover.xhtml"
    navigation_document: str = "_nav.xhtml"
    ncx_document: str = "_toc.ncx"
    # Project files
    metadata: str = "_metadata"
    nav: str = "_nav"
