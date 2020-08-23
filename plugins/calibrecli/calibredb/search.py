import os
import subprocess
from typing import List, Optional


def search(
    search_expression_: str,
    portable: Optional[str] = "",
    help_: Optional[bool] = None,
    with_library_: Optional[str] = None,
    password_: Optional[str] = None,
    username_: Optional[str] = None,
    version_: Optional[bool] = None,
    limit_: Optional[str] = None
) -> List[str]:
    """
    https://manual.calibre-ebook.com/generated/en/calibredb.html#search
    """
    args = [os.path.join(portable, "calibredb"), "search"]
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
    if limit_:
        args.extend(["--limit", limit_])
    args.append(search_expression_)
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            check=True,
            encoding="utf-8"
        )
    except subprocess.CalledProcessError:
        return []
    return result.stdout.split(",")
