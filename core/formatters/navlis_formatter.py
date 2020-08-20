from .base_formatter import BaseFormatter


class NavlisFormatter(BaseFormatter):
    def run(
        self,
        indents: int
    ) -> str:
        return "".join(
            [
                nav_node.get_nav_li(
                    indents=indents,
                    root_dir=self.package_contents.src
                )
                for nav_node in self.package_contents.nav_nodes
            ]
        ).strip()
