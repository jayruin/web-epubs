from argparse import ArgumentParser
import os
from pathlib import Path
import sys


def make_project_argparser(description: str) -> ArgumentParser:
    cwd = Path(os.getcwd())
    script = Path(sys.argv[0])
    relative_script = script.relative_to(cwd)
    if relative_script.name == "__main__.py":
        module_parts = relative_script.parent.parts
    else:
        module_parts = relative_script.with_suffix("").parts
    module = ".".join(module_parts)
    parser = ArgumentParser(
        prog=f"python -m {module}",
        description=description
    )
    add_project_argparser_args(parser)

    return parser


def add_project_argparser_args(parser: ArgumentParser) -> None:
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
        "--bundles-directory",
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
        nargs="*"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all projects"
    )
