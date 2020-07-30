import os
import subprocess
from typing import Optional


def calibre(
    path_to_ebook_: Optional[str] = None,
    portable: Optional[str] = "",
    detach_: Optional[bool] = None,
    help_: Optional[bool] = None,
    ignore_plugins_: Optional[bool] = None,
    no_update_check_: Optional[bool] = None,
    shutdown_running_calibre_: Optional[bool] = None,
    start_in_tray_: Optional[bool] = None,
    version_: Optional[bool] = None,
    with_library_: Optional[str] = None
) -> None:
    """
    https://manual.calibre-ebook.com/generated/en/calibre.html
    """
    args = [os.path.join(portable, "calibre")]
    if detach_:
        args.append("--detach")
    if help_:
        args.append("--help")
    if ignore_plugins_:
        args.append("--ignore-plugins")
    if no_update_check_:
        args.append("--no-update-check")
    if shutdown_running_calibre_:
        args.append("--shutdown-running-calibre")
    if start_in_tray_:
        args.append("--start-in-tray")
    if version_:
        args.append("--version")
    if with_library_:
        args.extend(["--with-library", with_library_])
    if path_to_ebook_:
        args.append(path_to_ebook_)
    subprocess.run(args, check=True)
