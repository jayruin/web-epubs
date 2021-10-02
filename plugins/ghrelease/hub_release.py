from typing import Optional

from core.commands import command


# https://hub.github.com/hub-release.1.html

@command(["hub", "release", "create"], flag_repeats={"attach"})
def create(
    tag: str,
    /, *,
    draft: bool = False,
    prerelease: bool = False,
    browse: bool = False,
    copy: bool = False,
    attach: Optional[list[str]] = None,
    message: Optional[str] = None,
    file: Optional[str] = None,
    commitish: Optional[str] = None,
) -> str:
    return ""


@command(["hub", "release", "delete"])
def delete(tag: str, /) -> str:
    return ""
