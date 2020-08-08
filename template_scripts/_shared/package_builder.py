from collections import OrderedDict
import datetime
import itertools
import json
import mimetypes
from pathlib import Path
import shutil
from typing import List

import template_scripts._shared.constants as constants
from template_scripts._shared.cover import create_default_cover
from template_scripts._shared.metadata import Metadata
from template_scripts._shared.nav_node import NavNode
from template_scripts._shared.package_copier import PackageCopier


class PackageBuilder:
    def __init__(
        self,
        src: str,
        dst: str,
        template_dir: str
    ) -> None:
        self.src: str = src
        self.dst: str = dst
        self.template_dir: str = template_dir

        self.metadata: Metadata = Metadata.from_json_path(
            Path(
                self.src,
                constants.METADATA_JSON
            )
        )

        shutil.rmtree(self.dst, ignore_errors=True)

        self.manifest_files_to_ignore: List[str] = []
        self.manifest_files_to_ignore.append(self.metadata.cover)

        with open(Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.TEMPLATE_XHTML
        ), "r", encoding="utf-8") as f:
            template_str = f.read()
        self.html_copier: PackageCopier = PackageCopier(
            src=self.src,
            dst=str(Path(self.dst, constants.ROOT_PATH_DIR)),
            template_str=template_str,
            template_indents=3
        )

        self.template_copier: PackageCopier = PackageCopier(
            src=self.template_dir,
            dst=self.dst,
            template_str=template_str,
            template_indents=3
        )

        with open(Path(
            self.src,
            constants.NAV_JSON
        ), "r", encoding="utf-8") as f:
            content = f.read()
        self.nav_nodes: List[NavNode] = [
            NavNode.from_dict(d)
            for d in json.loads(content)
        ]

    def _write_contents_from_template(
        self
    ) -> None:
        self.template_copier.copy_over()
        self.html_copier.copy_over()

    def _write_nav_toc_xhtml(
        self
    ) -> None:
        with open(Path(
            self.src,
            constants.NAV_JSON
        ), "r", encoding="utf-8") as f:
            nav_lis = "".join(
                [
                    nav_node.get_nav_li(
                        indents=5,
                        root_dir=self.src
                    )
                    for nav_node in self.nav_nodes
                ]
            ).strip()
        with open(Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.TOC_XHTML
        ), "r", encoding="utf-8") as f:
            content = f.read()
        content = content.format(
            nav=nav_lis
        )
        with open(Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            constants.TOC_XHTML
        ), "w", encoding="utf-8") as f:
            f.write(content)
        with open(Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.NAV_XHTML
        ), "r", encoding="utf-8") as f:
            content = f.read()
        content = content.format(
            nav=nav_lis
        )
        with open(Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            constants.NAV_XHTML
        ), "w", encoding="utf-8") as f:
            f.write(content)

    def _write_cover_xhtml(
        self
    ) -> None:
        cover_src = Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.COVER_XHTML
        )
        cover_dst = Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            constants.COVER_XHTML
        )
        with open(cover_src, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.format(
            cover_file=self.metadata.cover
        )
        with open(cover_dst, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_package_opf(
        self
    ) -> None:
        with open(Path(
            self.template_dir,
            constants.ROOT_PATH_DIR,
            constants.PACKAGE_OPF
        ), "r", encoding="utf-8") as f:
            content = f.read()
        content = content.format(
            languages="".join(
                [
                    f"{constants.INDENT * 2}"
                    f"<dc:language>{language}</dc:language>\n"
                    for language in self.metadata.languages
                ]
            ).strip(),
            title=self.metadata.title,
            author=self.metadata.author,
            date=self.metadata.date,
            modified=constants.BUILD_TIME,
            cover_file=self.metadata.cover,
            cover_media_type=mimetypes.guess_type(self.metadata.cover)[0],
            manifest="".join(
                [
                    f"{constants.INDENT * 2}<"
                    "item href=\"{href}\""
                    " id=\"{id}\""
                    " media-type=\"{media_type}\""
                    "/>\n".format(
                        href=key,
                        id=val,
                        media_type=mimetypes.guess_type(key)[0]
                    )
                    for key, val in self.html_copier.manifest_file_ids.items()
                    if key not in self.manifest_files_to_ignore
                ]
            ).strip(),
            spine="".join(
                [
                    f"{constants.INDENT * 2}<"
                    "itemref idref=\"{idref}\""
                    " linear=\"yes\""
                    "/>\n".format(
                        idref=self.html_copier.manifest_file_ids[href]
                    )
                    for href in list(
                        OrderedDict.fromkeys(
                            itertools.chain.from_iterable(
                                [
                                    nav_node.get_spine_hrefs()
                                    for nav_node in self.nav_nodes
                                ]
                            )
                        )
                    )
                ]
            ).strip()
        )
        with open(Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            constants.PACKAGE_OPF
        ), "w", encoding="utf-8") as f:
            f.write(content)

    def _create_default_cover_if_needed(
        self
    ) -> None:
        cover_path = Path(
            self.dst,
            constants.ROOT_PATH_DIR,
            self.metadata.cover
        )

        if not cover_path.exists():
            create_default_cover(cover_path)

    def build(
        self
    ) -> None:
        self._write_contents_from_template()
        self._write_nav_toc_xhtml()
        self._write_cover_xhtml()
        self._write_package_opf()
        self._create_default_cover_if_needed()
