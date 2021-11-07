from argparse import Namespace
from pathlib import Path

from app import make_main_argparser


def parse_args() -> Namespace:
    description = "Working with PDF files"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser", required=True)

    pagimg_parser = subparsers.add_parser(
        "from-pagimg",
        description="Convert pagimg project to PDF"
    )
    pagimg_parser.add_argument("directory", type=Path)
    pagimg_parser.add_argument("pdf_file", type=Path)
    pagimg_parser.set_defaults(run=from_pagimg_from_args)

    args = parser.parse_args()
    return args


def from_pagimg_from_args(args: Namespace) -> None:
    pass


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
