from argparse import Namespace
from pathlib import Path

from .arrange import arrange
from .autonav import autonav
from app import make_main_argparser, make_parent_argparser, Settings
from app.workers import Librarian
from core.project import EPUBProject
from core.serialize import write_nav


def parse_args() -> Namespace:
    description = "Tools for paginated images"
    parser = make_main_argparser(description)
    subparsers = parser.add_subparsers(dest="subparser")
    parent_parser = make_parent_argparser()

    arrange_parser = subparsers.add_parser(
        "arrange",
        description="Arrange files"
    )
    arrange_parser.add_argument("-s", "--suffixes", nargs="*")
    arrange_parser.add_argument("directory", type=Path)
    arrange_parser.set_defaults(run=arrange_from_args)

    autonav_parser = subparsers.add_parser(
        "autonav",
        description="Generate _nav",
        parents=[parent_parser]
    )
    autonav_parser.add_argument(
        "--nav-format",
        default="json",
        choices={"json", "yaml"}
    )
    autonav_parser.set_defaults(run=autonav_from_args)

    args = parser.parse_args()
    return args


def arrange_from_args(args: Namespace) -> None:
    arrange(args.directory, args.suffixes)


def autonav_from_args(args: Namespace) -> None:
    settings = Settings.from_namespace(args)
    projects: list[str]
    if args.all:
        librarian = Librarian(settings)
        projects = librarian.get_projects()
    else:
        projects = args.projects
    for project in projects:
        project_path = Path(settings.projects_directory, project)
        root_tree = autonav(project_path, root=project_path)
        if root_tree is not None:
            nav_trees = root_tree.children
            nav_file = Path(
                project_path,
                EPUBProject.NAV
            ).with_suffix(f".{args.nav_format}")
            write_nav(nav_file, nav_trees)


def main() -> None:
    args = parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
