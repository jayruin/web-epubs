from collections.abc import Callable, Collection, Iterable, Mapping
from functools import wraps
from inspect import Parameter, signature
from subprocess import CalledProcessError
from typing import Any, cast, Optional, ParamSpec, TypeVar

from .processing import identity
from core.runner import subprocess_run


_P = ParamSpec("_P")
_R = TypeVar("_R")


def command(
    executable: Iterable[str],
    flag_overrides: Mapping[str, str] = {},
    flag_repeats: Collection[str] = set(),
    processing: Callable[[str], _R] = identity,
    check_returncode: bool = True
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    def decorator(function: Callable[_P, _R]) -> Callable[_P, _R]:
        @wraps(function)
        def decorated(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            subprocess_args: list[str] = list(executable)
            sig = signature(function)
            ba = sig.bind(*args, **kwargs)
            ba.apply_defaults()
            for name, value in ba.arguments.items():
                param = sig.parameters[name]
                positional = param.kind == Parameter.POSITIONAL_ONLY
                flag_override = flag_overrides.get(name)
                flag_repeat = name in flag_repeats
                subprocess_args.extend(
                    format_arg(
                        name,
                        value,
                        positional,
                        flag_override,
                        flag_repeat
                    )
                )
            try:
                command_output = subprocess_run(
                    subprocess_args,
                    check_returncode=check_returncode
                )
                return processing(command_output)
            except CalledProcessError:
                return function(*args, **kwargs)
        return decorated
    return decorator


def format_arg(
    name: str,
    value: Any,
    positional: bool,
    flag_override: Optional[str] = None,
    flag_repeat: bool = False
) -> Iterable[str]:
    if not value:
        return
    if positional:
        flag = None
    elif flag_override:
        flag = flag_override
    else:
        flag = format_flag(name)
    iterable_exclusions = (str, bytes)
    if isinstance(value, bool):
        if flag:
            yield flag
    elif (
        isinstance(value, Iterable)
        and not isinstance(value, iterable_exclusions)
    ):
        value = cast(Iterable[Any], value)
        if flag_repeat:
            for item in value:
                if flag:
                    yield flag
                yield str(item)
        else:
            if flag:
                yield flag
            for item in value:
                yield str(item)
    else:
        if flag:
            yield flag
        yield str(value)


def format_flag(name: str) -> str:
    return "--" + name.rstrip("_").replace("_", "-")
