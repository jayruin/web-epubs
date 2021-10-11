from enum import Enum, unique


@unique
class EPUBType(Enum):
    PAGINATED_IMAGES = "pagimg"
    EPUB2 = "epub2"
    EPUB3 = "epub3"
