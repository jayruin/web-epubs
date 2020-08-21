from .text_writer import TextWriter


class Utf8Writer(TextWriter):
    def __init__(
        self
    ) -> None:
        super(Utf8Writer, self).__init__(encoding="utf-8")
