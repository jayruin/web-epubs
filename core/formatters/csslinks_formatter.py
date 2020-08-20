from core import constants
from core.formatters.base_formatter import BaseFormatter


class CsslinksFormatter(BaseFormatter):
    def run(
        self,
        indents: int
    ) -> str:
        return "".join(
            [
                f"{constants.INDENT * indents}<"
                "link href=\"{href}\""
                " rel=\"stylesheet\""
                " type=\"text/css\""
                "/>\n".format(
                    href=css_file
                )
                for css_file in self.package_contents.css_files
            ]
        ).strip()
