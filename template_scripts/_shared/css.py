from typing import List

import template_scripts._shared.constants as constants


def generate_css_links(
    css_files: List[str],
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
            for css_file in css_files
        ]
    ).strip()
