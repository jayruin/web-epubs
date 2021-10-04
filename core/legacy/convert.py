from argparse import ArgumentParser
import json
from pathlib import Path

from .nav_node import NavNode
from core.project.anchor import Anchor
from core.project.tree import Tree


def navnode_to_tree(navnode: NavNode, root_dir: str) -> Tree[Anchor]:
    href = Path(navnode.value)
    text = navnode.get_content(root_dir)
    anchor = Anchor(text, href)
    children = [
        navnode_to_tree(child, root_dir) for child in navnode.children
    ]
    return Tree[Anchor](anchor, children)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    args = parser.parse_args()
    with open(args.old, "rb") as f:
        nav_nodes = [NavNode.from_dict(d) for d in json.load(f)]
    nav_trees = [
        navnode_to_tree(nav_node, args.old.parent)
        for nav_node in nav_nodes
    ]
    with open(args.new, "w", encoding="utf-8") as f:
        json.dump(nav_trees, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
