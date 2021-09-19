from argparse import ArgumentParser
import os
from pathlib import Path
import sys


def make_project_argparser(description: str) -> ArgumentParser:
    cwd = Path(os.getcwd())
    script = Path(sys.argv[0])
    module_parts = script.relative_to(cwd).with_suffix("").parts
    module = ".".join(module_parts)
    parser = ArgumentParser(
        prog=f"python -m {module}",
        description=description
    )

    parser.add_argument(
        "--projects-directory",
        type=Path
    )
    parser.add_argument(
        "--expanded_epubs_directory",
        type=Path
    )
    parser.add_argument(
        "--packaged_epubs_directory",
        type=Path
    )
    parser.add_argument(
        "--epubcheck-directory",
        type=Path
    )
    parser.add_argument(
        "--logs-directory",
        type=Path
    )

    parser.add_argument(
        "projects",
        help=" ".join(
            [
                "List of projects.",
                "Each project should be a subdirectory of PROJECTS_DIRECTORY."
            ]
        ),
        nargs="+"
    )

    return parser
