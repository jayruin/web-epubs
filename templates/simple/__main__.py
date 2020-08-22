import os
import sys

from templates.simple._builder import SimpleBuilder


for arg in sys.argv[1:]:
    template_dir = "./templates/simple/contents"
    src = os.path.join("./html", arg)
    dst = os.path.join("./epub", arg)
    pb = SimpleBuilder(src, dst, template_dir)
    pb.build()
