from argparse import Namespace
from pathlib import Path

from .arrange import arrange
from app import make_main_argparser


def parse_args() -> Namespace:
    description = "Tools for paginated images"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser")

    arrange_parser = subparsers.add_parser(
        "arrange",
        description="Arrange files"
    )
    arrange_parser.add_argument("-s", "--suffixes", nargs="*")
    arrange_parser.add_argument("directory", type=Path)
    arrange_parser.set_defaults(run=arrange_from_args)

    args = parser.parse_args()
    return args


def arrange_from_args(args: Namespace) -> None:
    arrange(args.directory, args.suffixes)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
