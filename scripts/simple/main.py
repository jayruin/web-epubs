import os
from pathlib import Path
import sys

root = str(Path(__file__).resolve().parents[2])
sys.path.append(root)
os.chdir(root)

from scripts._shared.package_builder import PackageBuilder  # noqa E402


def main():
    for arg in sys.argv[1:]:
        template_dir = "./templates/simple"
        src = os.path.join("./html", arg)
        dst = os.path.join("./epub", arg)
        pb = PackageBuilder(src, dst, template_dir)
        pb.build()


if __name__ == "__main__":
    main()
