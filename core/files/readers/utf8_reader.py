from .text_reader import TextReader


class Utf8Reader(TextReader):
    def __init__(
        self
    ) -> None:
        super(Utf8Reader, self).__init__(encoding="utf-8")
