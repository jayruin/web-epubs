import os

from ._builder import Epub2Builder
from core import constants
from core.argparsers import parser_projects_only


module_name = "templates.epub2"
description = "Create ePub contents from epub2 template."
parser = parser_projects_only(module_name, description, False)
args = parser.parse_args()
for project in args.projects:
    template_dir = "./templates/epub2/contents"
    src = os.path.join(constants.HTML_DIRECTORY, project)
    dst = os.path.join(constants.EPUB_DIRECTORY, project)
    pb = Epub2Builder(src, dst, template_dir)
    pb.build()
