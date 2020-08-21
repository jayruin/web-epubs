import os
from pathlib import Path
import sys

root = str(Path(__file__).resolve().parents[2])
sys.path.append(root)
os.chdir(root)

from templates.simple.builder import Builder  # noqa E402


def main():
    for arg in sys.argv[1:]:
        template_dir = "./templates/simple/contents"
        src = os.path.join("./html", arg)
        dst = os.path.join("./epub", arg)
        pb = Builder(src, dst, template_dir)
        pb.build()


if __name__ == "__main__":
    main()
