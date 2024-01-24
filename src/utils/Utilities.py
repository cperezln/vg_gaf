from ..gramian.gramian import GramianAngularField
from ..visibility.horizontal.hvg import HorizontalVisibilityGraph
import numpy as np
from random import gauss
from pandas import Series
import networkx as net


def gramian_projection(GAF: GramianAngularField):
    """
    Given a Gramian Angular Field matrix representation, computes it corresponding HVG.
    :param GAF: GramianAngularField (difference) to compute its corresponding HVG
    :return hvg: HorizontalVisibilityGraph
    """
    if GAF.op_type != 'dif' or GAF.function != np.sin:
        raise ValueError("Cannot compute Gramian Projection of a not sin difference GAF.")
    m = GAF.matrix
    ln = len(m)
    rm = [[0]*ln for _ in range(ln)]
    for i in range(ln):
        h = -2
        for j in range(i + 1, ln):
            if m[i][j] > 0 or m[i][j] == h:
                rm[i][j] = 1
                rm[j][i] = 1
                break
            elif m[i][j] < 0 and m[i][j] > h:
                rm[i][j] = 1
                rm[j][i] = 1
                h = m[i][j]
            elif m[i][j] == 0:
                rm[i][j] = i + 1 == j
                rm[j][i] = i + 1 == j
            elif m[i][j] < 0 and m[i][j] <= h:
                pass
    hvg = HorizontalVisibilityGraph(rm)
    return hvg

def white_noise(n):
    """
    Return a white noise series of lenght n.
    :param n: lenght of the series
    :return: Series of Gaussian White Noise
    """
    ts = [gauss(0, 1) for i in range(n)]
    return Series(ts)

def average_path_lenght(g: net.Graph):
    """
    Given a networkx Graph, returns it average path lenght (using Floyd-Warshall's algorithm to compute peers lenght)
    :param g: nx.Graph:
    :return: average path lenght
    """
    res = net.floyd_warshall(g)
    fact = len(g)*(len(g)-1)
    return sum((1/fact)*np.array([res[i][j] for i in res for j in res[i]]))