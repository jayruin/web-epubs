from enum import Enum, unique


@unique
class EPUBType(Enum):
    EPUB2 = "epub2"
    EPUB3 = "epub3"
