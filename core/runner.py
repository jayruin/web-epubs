import argparse
import os
import pathlib
import subprocess
import sys

from core.constants import Encoding


def make_project_argparser(description: str) -> argparse.ArgumentParser:
    cwd = pathlib.Path(os.getcwd())
    script = pathlib.Path(sys.argv[0])
    module_parts = script.relative_to(cwd).with_suffix("").parts
    module = ".".join(module_parts)
    parser = argparse.ArgumentParser(
        prog=f"python -m {module}",
        description=description
    )

    parser.add_argument(
        "--projects-directory",
        type=pathlib.Path
    )
    parser.add_argument(
        "--expanded_epubs_directory",
        type=pathlib.Path
    )
    parser.add_argument(
        "--packaged_epubs_directory",
        type=pathlib.Path
    )
    parser.add_argument(
        "--epubcheck-directory",
        type=pathlib.Path
    )
    parser.add_argument(
        "--logs-directory",
        type=pathlib.Path
    )
    parser.add_argument(
        "--bundles-directory",
        type=pathlib.Path
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

    return parser


def subprocess_run(args: list[str]) -> str:
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding=Encoding.UTF_8.value
    )
    completed_process.check_returncode()
    return completed_process.stdout
