from collections import defaultdict
import math

from PIL import Image


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    image_aspect_ratio = image.size[0] / image.size[1]
    target_aspect_ratio = width / height
    if target_aspect_ratio > image_aspect_ratio:
        resized_width = int(image_aspect_ratio * height)
        resized_height = height
    else:
        resized_width = width
        resized_height = int(width / image_aspect_ratio)
    resized_image = image.resize((resized_width, resized_height))
    offset_x = int((width - resized_width) / 2)
    offset_y = int((height - resized_height) / 2)
    offset = (offset_x, offset_y)
    target_image = Image.new("RGB", (width, height))
    target_image.paste(resized_image, offset)
    return target_image


def get_grid_item_size(images: list[Image.Image]) -> tuple[int, int]:
    aspect_ratios: dict[float, list[Image.Image]] = defaultdict(list)
    for image in images:
        aspect_ratio = image.size[0] / image.size[1]
        aspect_ratios[aspect_ratio].append(image)
    return min(
        max(
            aspect_ratios.values(),
            key=lambda l: len(l)
        ),
        key=lambda i: i.size[0] * i.size[1]
    ).size


def make_grid_cover(covers: list[Image.Image]) -> Image.Image:
    grid_item_width, grid_item_height = get_grid_item_size(covers)
    grid_dimension = math.ceil(math.sqrt(len(covers)))
    grid_width = grid_item_width * grid_dimension
    grid_height = grid_item_height * grid_dimension
    grid = Image.new("RGB", (grid_width, grid_height))
    for i, cover in enumerate(covers):
        resized_cover = fit(cover, grid_item_width, grid_item_height)
        row = i // grid_dimension
        column = i % grid_dimension
        offset_x = grid_item_width * column
        offset_y = grid_item_height * row
        offset = (offset_x, offset_y)
        grid.paste(resized_cover, offset)
    return grid
