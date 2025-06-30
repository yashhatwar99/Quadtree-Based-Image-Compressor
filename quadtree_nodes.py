
import numpy as np


class QuadTreeNode:
    """ Base quad tree data structure that handles the positioning, subdivision and rendering of nodes. """

    def __init__(self, position: tuple, size: tuple):
        self.position = position
        self.size = size
        self.color = None
        self.is_subdivided = False
        self.bottom_left_node = None
        self.bottom_right_node = None
        self.top_left_node = None
        self.top_right_node = None

    def _create_child_node(self, position, size):
        return QuadTreeNode(position, size)

    def subdivide(self):
        """ Splits the current quad into 4 child quads if this is possible.
        :return: Child quads or None or an empty list if it cannot be further subdivided.
        """
        if self.is_subdivided:
            return []

        width, height = self.size
        x, y = self.position

        if width <= 1 or height <= 1:
            return []

        self.is_subdivided = True

        split_width = width // 2
        split_height = height // 2

        self.bottom_left_node = self._create_child_node(
            (x, y),
            (split_width, split_height))

        self.bottom_right_node = self._create_child_node(
            (x + split_width, y),
            (width - split_width, split_height))

        self.top_left_node = self._create_child_node(
            (x, y + split_height),
            (split_width, height - split_height))

        self.top_right_node = self._create_child_node(
            (x + split_width, y + split_height),
            (width - split_width, height - split_height))

        return self.bottom_left_node, self.bottom_right_node, self.top_left_node, self.top_right_node

    def draw(self, image_data: np.array):
        if self.is_subdivided:
            self.bottom_left_node.draw(image_data)
            self.bottom_right_node.draw(image_data)
            self.top_left_node.draw(image_data)
            self.top_right_node.draw(image_data)
        else:
            self.draw_self(image_data)

    def draw_self(self, image_data: np.array):
        if self.color is None:
            return
        start_x, start_y = self.position
        width, height = self.size
        end_x = start_x + width
        end_y = start_y + height
        image_data[start_y: end_y, start_x: end_x] = self.color


class CompressNode(QuadTreeNode):
    """ QuadTree node used for incrementally compressing an image. """

    def __init__(self, position, image_data: np.array):
        height, width, _ = image_data.shape
        super().__init__(position, (width, height))

        self.image_data = image_data

        # Compute the detail as the sum of the standard deviation of each channel (RGB)
        # weighted by the number of pixels in this region.
        self.detail = np.sum(np.std(image_data, axis=(0, 1))) * self.image_data.size
        self.color = np.mean(image_data, axis=(0, 1)).astype(np.uint8)

    def _create_child_node(self, position, size):
        width, height = size
        child_x, child_y = position
        own_x, own_y = self.position

        start_x = child_x - own_x
        start_y = child_y - own_y
        return CompressNode(position, self.image_data[start_y: start_y + height, start_x: start_x + width])

    def subdivide(self):
        nodes = super().subdivide()
        # Memory of the image is no longer needed as the relevant areas
        # have been passed on to the child nodes.
        self.image_data = None
        return nodes

    def extract_data(self, subdivided_flags, colors):
        subdivided_flags.append(self.is_subdivided)

        if self.is_subdivided:
            self.bottom_left_node.extract_data(subdivided_flags, colors)
            self.bottom_right_node.extract_data(subdivided_flags, colors)
            self.top_left_node.extract_data(subdivided_flags, colors)
            self.top_right_node.extract_data(subdivided_flags, colors)
        else:
            r, g, b = self.color
            colors.append((int(r), int(g), int(b)))


class ReconstructNode(QuadTreeNode):
    """ QuadTree node for reconstructing a compressed image. """

    def __init__(self, position, size, subdivided_flags: list, colors: list):
        super().__init__(position, size)

        self._subdivided_flags = subdivided_flags
        self._colors = colors

        is_subdivided = subdivided_flags.pop()
        if is_subdivided:
            self.subdivide()
        else:
            self.color = colors.pop()

    def _create_child_node(self, position, size):
        return ReconstructNode(position, size, self._subdivided_flags, self._colors)
