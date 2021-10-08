from pathlib import Path

from app import make_project_argparser, Settings
from app.workers import Checker


description = "Check EPUBs"
parser = make_project_argparser(description)
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
checker = Checker(settings)
checker.check_projects(projects, args.type)
