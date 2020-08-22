import os
import sys

from core import constants
from templates.simple._builder import SimpleBuilder


for arg in sys.argv[1:]:
    template_dir = "./templates/simple/contents"
    src = os.path.join(constants.HTML_DIRECTORY, arg)
    dst = os.path.join(constants.EPUB_DIRECTORY, arg)
    pb = SimpleBuilder(src, dst, template_dir)
    pb.build()
