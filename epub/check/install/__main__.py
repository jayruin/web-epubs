from app import make_project_argparser, Settings
from app.workers import Installer


description = "Install EPUBCheck"
parser = make_project_argparser(description)
args = parser.parse_args()
settings = Settings.from_namespace(args)
installer = Installer(settings)
installer.install_epubcheck()
