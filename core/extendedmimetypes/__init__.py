import json
import mimetypes
from pathlib import Path

for entry in Path("core", "extendedmimetypes").iterdir():
    if entry.is_file() and entry.name.endswith(".json"):
        with open(entry, "rb") as f:
            mapping = json.load(f)
            for file_ext, file_type in mapping.items():
                mimetypes.add_type(file_type, file_ext)
