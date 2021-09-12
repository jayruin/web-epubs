from core.config import NavNode
from core.project.anchor import Anchor
from core.project.tree import Tree


def navnode_to_tree(navnode: NavNode, root_dir: str) -> Tree[Anchor]:
    href = navnode.value
    text = navnode.get_content(root_dir)
    anchor = Anchor(href, text)
    children = [
        navnode_to_tree(child, root_dir) for child in navnode.children
    ]
    return Tree[Anchor](anchor, children)
