import os
import subprocess
from typing import Optional


def ebook_viewer(
    file_: str,
    portable: Optional[str] = "",
    continue_: Optional[bool] = None,
    detach_: Optional[bool] = None,
    force_reload_: Optional[bool] = None,
    full_screen_: Optional[bool] = None,
    help_: Optional[bool] = None,
    open_at_: Optional[bool] = None,
    raise_window_: Optional[bool] = None,
    version_: Optional[bool] = None
) -> None:
    """
    https://manual.calibre-ebook.com/generated/en/ebook-viewer.html
    """
    args = [os.path.join(portable, "ebook-viewer")]
    if continue_:
        args.append("--continue")
    if detach_:
        args.append("--detach")
    if force_reload_:
        args.append("--force-reload")
    if full_screen_:
        args.append("--full-screen")
    if help_:
        args.append("--help")
    if open_at_:
        args.append("--open-at")
    if raise_window_:
        args.append("--raise-window")
    if version_:
        args.append("--version")
    args.append(file_)
    result = subprocess.run(args, check=True)
