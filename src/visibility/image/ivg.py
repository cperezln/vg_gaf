import numpy as np
import networkx as net


def is_visible(x, horizontal=False):
    n = len(x)
    if n <= 2:
        return True
    if not horizontal:
        aux = (x[n - 1] - x[0]) / (n - 1)
        return all(x[k] < x[0] + k * aux for k in range(1, n - 1))
    else:
        aux = min(x[0], x[n - 1])
        return all(x[k] < aux for k in range(1, n - 1))


class IVG:
    __nx = None
    __datastructure = None
    horizontal = None
    size = None

    def __init__(self, image, horizontal=False):
        """
        Generate an image (horizontal) visibility graph for a given image
        :param image: image as a 2D-list
        :param horizontal: type of visibility graph (regular or horizontal)
        :return graph: set of edges
        """
        self.__horizontal = horizontal
        if all(len(row) == len(image) for row in image):
            self.size = len(image)
        else:
            raise ValueError("Invalid image. Size must be square")
        n = self.size
        edges = set()
        for i, j in np.ndindex(n, n):
            for k in range(1, n - j):
                if is_visible([image[i][j + m] for m in range(k + 1)], horizontal):
                    edges.add(((i, j), (i, j + k)))
            for k in range(1, n - i):
                if is_visible([image[i + m][j] for m in range(k + 1)], horizontal):
                    edges.add(((i, j), (i + k, j)))
            for k in range(1, min(n - i, n - j)):
                if is_visible([image[i + m][j + m] for m in range(k + 1)], horizontal):
                    edges.add(((i, j), (i + k, j + k)))
            for k in range(1, min(n - i, j)):
                if is_visible([image[i + m][j - m] for m in range(k + 1)], horizontal):
                    edges.add(((i, j), (i + k, j - k)))
        self.__datastructure = edges

    @property
    def edges(self):
        return self.__datastructure

    @property
    def nx(self):
        if self.__nx is None:
            self.__nx = net.Graph(self.__datastructure)
        return self.__nx
