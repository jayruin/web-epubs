import json
import mimetypes
import os

with os.scandir("./core/extendedmimetypes/") as it:
    for entry in it:
        if entry.is_file() and entry.name.endswith(".json"):
            with open(entry, "r") as f:
                mapping = json.loads(f.read())
                for file_ext, file_type in mapping.items():
                    mimetypes.add_type(file_type, file_ext)