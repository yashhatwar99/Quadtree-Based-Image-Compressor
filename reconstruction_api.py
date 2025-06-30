
import numpy as np
from PIL import Image
from quadtree_nodes import ReconstructNode
from encoding import decode_image_data


def reconstruct_quadtree(data: bytes) -> ReconstructNode:
    """Reconstruct QuadTree from binary data"""
    width, height, subdivided_flags, colors = decode_image_data(data)

    # The ReconstructNode requires these to be reversed for performance reasons
    subdivided_flags = list(reversed(subdivided_flags))
    colors = list(reversed(colors))

    return ReconstructNode((0, 0), (width, height), subdivided_flags, colors)


def reconstruct_image_data(data: bytes) -> np.array:
    """Reconstruct image data from binary representation"""
    tree = reconstruct_quadtree(data)
    width, height = tree.size

    image_data = np.zeros((height, width, 3), dtype=np.uint8)
    tree.draw(image_data)
    return image_data


def reconstruct_image_from_file(compressed_image_file: str) -> Image:
    """Reconstruct image from compressed file"""
    with open(compressed_image_file, "rb") as file:
        data = file.read()

    image_data = reconstruct_image_data(data)
    return Image.fromarray(image_data)
