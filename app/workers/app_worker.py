from app import Settings


class AppWorker:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
