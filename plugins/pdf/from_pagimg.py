from pathlib import Path

from pikepdf import OutlineItem, Pdf
from PIL import Image

from core.datastructures import Tree
from plugins.pagimg.navigation import organize_pages
from plugins.pagimg.paginated_anchor import PaginatedAnchor


def add_tree(
    parent_list: list[OutlineItem],
    tree: Tree[PaginatedAnchor],
    pages: list[Path]
) -> int:
    page_number = -1
    if tree.value.pages:
        page_number = len(pages)
    pages.extend(tree.value.pages)
    children: list[OutlineItem] = []
    child_page_numbers = [
        add_tree(children, child_tree, pages)
        for child_tree in tree.children
    ]
    if page_number < 0:
        page_number = child_page_numbers[0]
    outline_item = OutlineItem(tree.value.text, page_number)
    outline_item.children.extend(children)
    parent_list.append(outline_item)
    return page_number


def from_pagimg(directory: Path, pdf_file: Path) -> None:
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory!")
    if pdf_file.suffix != ".pdf":
        raise ValueError(f"{pdf_file} is not a PDF file!")
    root_tree = organize_pages(directory, directory)
    if root_tree is None:
        return
    pages: list[Path] = []
    outline_items: list[OutlineItem] = []
    for tree in root_tree.children:
        add_tree(outline_items, tree, pages)
    images: list[Image.Image] = []
    for page in pages:
        image = Image.open(page).convert("RGB")
        image.load()
        images.append(image)
    images[0].save(
        pdf_file,
        save_all=True,
        append_images=images[1:],
        resolution=300
    )
    with Pdf.open(pdf_file, allow_overwriting_input=True) as pdf:
        with pdf.open_outline() as outline:
            outline.root.extend(outline_items)
        pdf.save()
