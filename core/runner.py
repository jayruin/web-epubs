import collections.abc
import concurrent.futures
import contextlib

import subprocess
import typing

import tqdm

from core.constants import Encoding

_T = typing.TypeVar("_T")


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
