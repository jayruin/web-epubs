import mimetypes

from core import constants
from core.formatters.base_formatter import BaseFormatter


class ManifestitemsFormatter(BaseFormatter):
    def run(
        self,
        indents: int
    ) -> str:
        return "".join(
            [
                f"{constants.INDENT * indents}<"
                "item href=\"{href}\""
                " id=\"{id}\""
                " media-type=\"{media_type}\""
                "/>\n".format(
                    href=key,
                    id=val,
                    media_type=mimetypes.guess_type(key)[0]
                )
                for key, val in self.package_contents.file_id_mapping.items()
                if key not in self.manifest_files_to_ignore
            ]
        ).strip()
