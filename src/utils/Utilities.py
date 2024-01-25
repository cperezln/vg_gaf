from ..gramian.gramian import GramianAngularField
from ..visibility.horizontal.hvg import HorizontalVisibilityGraph
import numpy as np
from random import gauss
from pandas import Series
import networkx as net
import matplotlib.pyplot as plt
import cv2
import skimage


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

def generate_gafs(periodic: np.array, combination: np.array, method: str, func: callable):
    g = GramianAngularField(method, func, periodic)
    ng = GramianAngularField(method, func, combination)
    return g, ng

def plot_with_threshold(clean: GramianAngularField, noisy: GramianAngularField, threshold: float = 0.8, pool_func: callable = np.mean):
    def smooth(noisy: np.array, kernel_d: int = 2):
        kernel2 = np.ones((kernel_d, kernel_d), np.float32)/(kernel_d**2)
        # Applying the filter 
        smooth = cv2.filter2D(src=noisy, ddepth=-1, kernel=kernel2)
        return smooth
    
    def pool(smooth: np.array, k_size: int = 2):
        pooled = skimage.measure.block_reduce(smooth, (k_size,k_size), pool_func)
        return pooled

    aux = noisy.matrix.copy()
    aux[aux < threshold - 1] = -1
    aux[aux > 1-threshold] = 1

    smoothed = smooth(aux)

    pooled = pool(smoothed)
    pooled = cv2.resize(pooled, smoothed.shape)

    ax1 = plt.subplot(3, 2, 1)
    ax1.imshow(clean.matrix)
    ax1.set_title("Clean")

    ax2 = plt.subplot(3, 2, 2)
    ax2.imshow(noisy.matrix)
    ax2.set_title("Noisy")

    ax3 = plt.subplot(3, 2, (3, 4))
    ax3.imshow(aux)
    ax3.set_title("Noisy thresholded")

    ax4 = plt.subplot(3, 2, 5)
    ax4.imshow(smoothed)
    ax4.set_title(f"Noisy smooth")

    ax4 = plt.subplot(3, 2, 6)
    ax4.imshow(pooled)
    ax4.set_title(f"Final")
