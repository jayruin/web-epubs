from argparse import ArgumentParser, Namespace
import logging
from pathlib import Path
from typing import Optional

from .path_hash import check_path_hash, create_path_hash
from app import make_main_argparser
from core.constants import Encoding
from core.deserialize import get_load
from core.serialize import get_dump


def make_logger(log_file: Optional[Path] = None) -> logging.Logger:
    logger = logging.getLogger("hash")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    if log_file is not None:
        file_handler = logging.FileHandler(
            log_file,
            encoding=Encoding.UTF_8.value
        )
        logger.addHandler(file_handler)
    return logger


def parse_args() -> Namespace:
    description = "Hashing files and directories"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser", required=True)

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

    check_parser = subparsers.add_parser(
        "check",
        description="Check hashes",
        parents=[parent_parser]
    )
    check_parser.add_argument(
        "--log-file",
        type=Path
    )
    check_parser.set_defaults(run=check_from_args)

    args = parser.parse_args()
    return args


def create_from_args(args: Namespace) -> None:
    path_hash = create_path_hash(args.path, args.algorithms)
    dump = get_dump(args.hashes.suffix)
    with open(args.hashes, "w", encoding=Encoding.UTF_8.value) as f:
        dump(path_hash, f)


def check_from_args(args: Namespace) -> None:
    logger = make_logger(args.log_file)
    load = get_load(args.hashes.suffix)
    with open(args.hashes, "rb") as f:
        expected_path_hash = load(f)
    check_path_hash(args.path, expected_path_hash, logger)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
