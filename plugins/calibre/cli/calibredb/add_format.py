import os
import subprocess
from typing import Optional


def add_format(
    id_: str,
    ebook_file_: str,
    portable: Optional[str] = "",
    help_: Optional[bool] = None,
    with_library_: Optional[str] = None,
    password_: Optional[str] = None,
    username_: Optional[str] = None,
    version_: Optional[bool] = None,
    dont_replace_: Optional[bool] = None
) -> None:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#add-format
    """
    args = [os.path.join(portable, "calibredb"), "add_format"]
    if help_:
        args.append("--help")
    if with_library_:
        args.extend(["--with-library", with_library_])
    if password_:
        args.extend(["--password", password_])
    if username_:
        args.extend(["--username", username_])
    if version_:
        args.append("--version")
    if dont_replace_:
        args.append("--dont-replace")
    args.append(id_)
    args.append(ebook_file_)
    subprocess.run(args, check=True)
