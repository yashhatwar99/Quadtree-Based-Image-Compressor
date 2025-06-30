
import numpy as np
from sortedcontainers import SortedListWithKey
from quadtree_nodes import CompressNode
from encoding import encode_image_data


class ImageCompressor:
    """ Helper class that manages the CompressNodes and allows you to incrementally add detail. """

    def __init__(self, image_data: np.array):
        self.areas = SortedListWithKey(key=lambda node: node.detail)
        self._image_shape = image_data.shape
        self.height, self.width, _ = self._image_shape

        self.root_node = CompressNode((0, 0), image_data)
        self.areas.add(self.root_node)

    def add_detail(self, max_iterations: int = 1, detail_error_threshold: float = 100):
        for i in range(max_iterations):
            if not self.areas:
                break

            node_with_most_detail = self.areas.pop()
            for node in node_with_most_detail.subdivide():
                if node.detail > detail_error_threshold:
                    self.areas.add(node)

            if i > max_iterations:
                break

    def draw(self):
        new_image_data = np.zeros(self._image_shape, dtype=np.uint8)
        self.root_node.draw(new_image_data)
        return new_image_data

    def extract_data(self):
        subdivided_flags = []
        colors = []

        self.root_node.extract_data(subdivided_flags, colors)

        return subdivided_flags, colors

    def encode_to_binary(self) -> bytes:
        subdivided_flags, colors = self.extract_data()
        return encode_image_data(self.width, self.height, subdivided_flags, colors)
