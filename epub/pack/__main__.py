from pathlib import Path

from app import make_project_argparser, Settings
from app.workers import Packer


description = "Pack EPUBs"
parser = make_project_argparser(description)
parser.add_argument(
    "-c", "--compression",
    default=0,
    type=int,
    choices=range(10),
    help="Compression level to use for the output .epub file."
)
args = parser.parse_args()
settings = Settings.from_namespace(args)
projects: list[str]
if args.all:
    projects = [
        path.name
        for path in Path(
            settings.expanded_epubs_directory,
            args.type
        ).iterdir()
        if path.is_dir()
    ]
else:
    projects = args.projects
packer = Packer(settings)
packer.pack_projects(projects, args.type, args.compression)
