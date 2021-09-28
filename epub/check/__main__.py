from pathlib import Path

from app import make_project_argparser, Settings
from epub.check import check_projects


def main() -> None:
    description = "Check EPUBs"
    parser = make_project_argparser(description)
    parser.add_argument(
        "-t", "--type",
        default="epub3"
    )
    args = parser.parse_args()
    settings = Settings.from_namespace(args)
    projects: list[str]
    if args.all:
        projects = [
            ".".join(path.stem.split(".")[:-1])
            for path in Path(
                settings.packaged_epubs_directory,
                args.type
            ).iterdir()
            if path.is_file() and path.suffix == ".epub"
        ]
    else:
        projects = args.projects
    check_projects(settings, projects, args.type)


if __name__ == "__main__":
    main()
