from core import constants
from core.formatters.base_formatter import BaseFormatter


class LanguagesFormatter(BaseFormatter):
    def run(
        self,
        indents: int
    ) -> str:
        return "".join(
            [
                f"{constants.INDENT * indents}"
                f"<dc:language>{language}</dc:language>\n"
                for language in self.package_contents.metadata.languages
            ]
        ).strip()
