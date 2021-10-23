from argparse import ArgumentParser, Namespace
from pathlib import Path

from .path_hash import create_path_hash
from app import make_main_argparser
from core.constants import Encoding
from core.serialize import get_dump


def parse_args() -> Namespace:
    description = "Hashing files and directories"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser")

    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "path",
        type=Path
    )
    parent_parser.add_argument(
        "hashes",
        type=Path
    )

    create_parser = subparsers.add_parser(
        "create",
        description="Create hashes",
        parents=[parent_parser]
    )
    create_parser.add_argument(
        "--algorithms",
        nargs="*"
    )
    create_parser.set_defaults(run=create_from_args)

    args = parser.parse_args()
    return args


def create_from_args(args: Namespace) -> None:
    path_hash = create_path_hash(args.path, args.algorithms)
    dump = get_dump(args.hashes.suffix)
    with open(args.hashes, "w", encoding=Encoding.UTF_8.value) as f:
        dump(path_hash, f)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
