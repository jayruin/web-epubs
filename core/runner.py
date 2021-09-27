import argparse
import collections.abc
import concurrent.futures
import contextlib
import os
import pathlib
import subprocess
import sys
import typing

import tqdm

from core.constants import Encoding

_T = typing.TypeVar("_T")


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


def pool_run(
    function: typing.Callable[..., _T],
    args_collection: collections.abc.Collection[
        collections.abc.Iterable[typing.Any]
    ],
    kwargs_collection: collections.abc.Collection[
        collections.abc.Mapping[str, typing.Any]
    ],
    executor_type: typing.Union[
        typing.Literal["process"],
        typing.Literal["thread"]
    ],
    max_workers: typing.Optional[int] = None,
    as_completed: bool = False,
    show_progress: bool = False
) -> collections.abc.Generator[_T, None, None]:
    assert len(args_collection) == len(kwargs_collection)
    with contextlib.ExitStack() as stack:
        executor: concurrent.futures.Executor
        if executor_type == "process":
            executor = stack.enter_context(
                concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
            )
        elif executor_type == "thread":
            executor = stack.enter_context(
                concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
            )
        else:
            raise ValueError("Invalid executor_type")
        pbar: typing.Optional[tqdm.tqdm] = None
        if show_progress:
            pbar = stack.enter_context(tqdm.tqdm(total=len(args_collection)))
        futures = [
            executor.submit(function, *args, **kwargs)
            for args, kwargs in zip(args_collection, kwargs_collection)
        ]
        for future in concurrent.futures.as_completed(futures):
            if as_completed:
                yield future.result()
            if show_progress and pbar:
                pbar.update(1)
        if not as_completed:
            for future in futures:
                yield future.result()


def subprocess_run(args: list[str], check_returncode: bool = False) -> str:
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding=Encoding.UTF_8.value
    )
    if check_returncode:
        completed_process.check_returncode()
    return completed_process.stdout
