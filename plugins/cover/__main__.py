from argparse import Namespace
from pathlib import Path

from .make_grid import make_grid_cover
from app import make_main_argparser


def parse_args() -> Namespace:
    description = "Generating covers."
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser", required=True)

    make_grid_parser = subparsers.add_parser(
        "make-grid",
        description="Create a grid cover from existing covers"
    )
    make_grid_parser.add_argument("covers", nargs="*", type=Path)
    make_grid_parser.add_argument("--output", type=Path)
    make_grid_parser.set_defaults(run=make_grid_from_args)

    args = parser.parse_args()
    return args


def make_grid_from_args(args: Namespace) -> None:
    grid = make_grid_cover(args.covers)
    grid.save(args.output)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
