from argparse import Namespace
from pathlib import Path

from .convert import convert
from app import make_main_argparser


def parse_args() -> Namespace:
    description = "Working with Markdown files"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser")

    create_parser = subparsers.add_parser(
        "convert",
        description="Convert Markdown files to HTML files"
    )
    create_parser.add_argument(
        "source",
        type=Path
    )
    create_parser.add_argument(
        "destination",
        type=Path
    )
    create_parser.add_argument(
        "--copy",
        action="store_true"
    )
    create_parser.set_defaults(run=convert_from_args)

    args = parser.parse_args()
    return args


def convert_from_args(args: Namespace) -> None:
    convert(args.source, args.destination, args.copy)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
