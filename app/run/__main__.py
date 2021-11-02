from argparse import Namespace

from app import make_main_argparser, make_parent_argparser, Settings
from app.workers import Builder, Checker, Installer, Librarian, Packer


def parse_args() -> Namespace:
    description = "Creating and Validating EPUBs"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser", required=True)
    parent_parser = make_parent_argparser()

    build_parser = subparsers.add_parser(
        "build",
        description="Build EPUBs",
        parents=[parent_parser]
    )
    build_parser.add_argument(
        "-b", "--bundles",
        nargs="+",
        default=[]
    )
    build_parser.set_defaults(run=build)

    pack_parser = subparsers.add_parser(
        "pack",
        description="Pack EPUBs",
        parents=[parent_parser]
    )
    pack_parser.add_argument(
        "-c", "--compression",
        default=0,
        type=int,
        choices=range(10),
        help="Compression level to use for the output .epub file"
    )
    pack_parser.set_defaults(run=pack)

    check_parser = subparsers.add_parser(
        "check",
        description="Check EPUBs",
        parents=[parent_parser]
    )
    check_parser.add_argument(
        "-i", "--install",
        action="store_true",
        help="Install EPUBCheck"
    )
    check_parser.set_defaults(run=check)

    args = parser.parse_args()
    return args


def build(args: Namespace) -> None:
    settings = Settings.from_namespace(args)
    projects: list[str]
    if args.all:
        librarian = Librarian(settings)
        projects = librarian.get_projects()
    else:
        projects = args.projects
    if len(projects) > 0:
        print("Building projects...")
        builder = Builder(settings)
        builder.build_projects(projects, args.type, args.bundles)


def pack(args: Namespace) -> None:
    settings = Settings.from_namespace(args)
    projects: list[str]
    if args.all:
        librarian = Librarian(settings)
        projects = librarian.get_expanded_epubs().get(args.type, [])
    else:
        projects = args.projects
    if len(projects) > 0:
        print("Packing projects...")
        packer = Packer(settings)
        packer.pack_projects(projects, args.type, args.compression)


def check(args: Namespace) -> None:
    settings = Settings.from_namespace(args)
    if args.install:
        print("Installing EPUBCheck...")
        installer = Installer(settings)
        installer.install_epubcheck()
    projects: list[str]
    if args.all:
        librarian = Librarian(settings)
        projects = librarian.get_packaged_epubs().get(args.type, [])
    else:
        projects = args.projects
    if len(projects) > 0:
        print("Checking projects...")
        checker = Checker(settings)
        checker.check_projects(projects, args.type)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
