import os

from core import constants
from core.argparsers import parser_projects_only
from templates.comicbook._builder import ComicbookBuilder


module_name = "templates.comicbook"
description = "Create ePub contents from comicbook template."
parser = parser_projects_only(module_name, description, False)
args = parser.parse_args()
for project in args.projects:
    template_dir = "./templates/comicbook/contents"
    src = os.path.join(constants.HTML_DIRECTORY, project)
    dst = os.path.join(constants.EPUB_DIRECTORY, project)
    pb = ComicbookBuilder(src, dst, template_dir)
    pb.build()
