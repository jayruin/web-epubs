from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from core.packaging.package_contents import PackageContents


class BaseFormatter(ABC):
    def __init__(
        self,
        package_contents: "PackageContents"
    ) -> None:
        self.package_contents: "PackageContents" = package_contents

    @abstractmethod
    def run(
        self,
        indents: int,
        target: Optional[Path] = None
    ) -> str:
        pass
