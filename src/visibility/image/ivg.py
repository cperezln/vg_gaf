import numpy as np
import networkx as net


def is_visible(x, horizontal=False):
    """
    Tests for visibility between first and last element of time series
    :param x: time series
    :param horizontal: type of visibility graph (regular or horizontal)
    :return: true if first and last elements are visible to each other, false otherwise
    """
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
    __horizontal = None
    __size = None

    def __init__(self, image, horizontal=False, diags=False):
        """
        Generate an image (horizontal) visibility graph for a given image
        :param image: image as a 2D-list
        :param horizontal: type of visibility graph (regular or horizontal)
        :return: set of edges
        """
        self.__horizontal = horizontal
        if all(len(row) == len(image) for row in image):
            self.size = len(image)
        else:
            raise ValueError("Invalid image. Size must be square")
        n = self.__size
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
            for k in range(1, min(n - i, j + 1)):
                if is_visible([image[i + m][j - m] for m in range(k + 1)], horizontal):
                    edges.add(((i, j), (i + k, j - k)))
            if diags:
                for k in range(1, min(n - i, int(np.floor((n - j + 1) / 2)))):
                    if is_visible([image[i + m][j + 2 * m] for m in range(k + 1)], horizontal):
                        edges.add(((i, j), (i + k, j + 2 * k)))
                for k in range(1, min(int(np.floor((n - i + 1) / 2)), n - j)):
                    if is_visible([image[i + 2 * m][j + m] for m in range(k + 1)], horizontal):
                        edges.add(((i, j), (i + 2 * k, j + k)))
                for k in range(1, min(n - i, int(np.floor(j / 2)) + 1)):
                    if is_visible([image[i + m][j - 2 * m] for m in range(k + 1)], horizontal):
                        edges.add(((i, j), (i + k, j - 2 * k)))
                for k in range(1, min(int(np.floor((n - i + 1) / 2)), j + 1)):
                    if is_visible([image[i + 2 * m][j - m] for m in range(k + 1)], horizontal):
                        edges.add(((i, j), (i + 2 * k, j - k)))
        self.__datastructure = edges

    @property
    def edges(self):
        return self.__datastructure

    @property
    def nx(self):
        if self.__nx is None:
            self.__nx = net.Graph(self.__datastructure)
        return self.__nx

    @property
    def horizontal():
        return self.__horizontal
    
    @property
    def size():
        return self.__size