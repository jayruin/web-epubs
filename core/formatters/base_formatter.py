from abc import ABC, abstractmethod

from template_scripts._shared.package_contents import PackageContents


class BaseFormatter(ABC):
    def __init__(
        self,
        package_contents: PackageContents
    ) -> None:
        self.package_contents: PackageContents = package_contents

    @abstractmethod
    def run(
        self,
        indents: int
    ) -> str:
        pass
