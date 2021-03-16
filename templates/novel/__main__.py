import os

from ._builder import NovelBuilder
from core import constants
from core.argparsers import parser_projects_only


module_name = "templates.novel"
description = "Create ePub contents from novel template."
parser = parser_projects_only(module_name, description, False)
args = parser.parse_args()
for project in args.projects:
    template_dir = "./templates/novel/contents"
    src = os.path.join(constants.HTML_DIRECTORY, project)
    dst = os.path.join(constants.EPUB_DIRECTORY, project)
    pb = NovelBuilder(src, dst, template_dir)
    pb.build()
