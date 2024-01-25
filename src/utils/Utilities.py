from ..gramian.gramian import GramianAngularField
from ..visibility.horizontal.hvg import HorizontalVisibilityGraph
from ..visibility.image.ivg import IVG
import numpy as np
from random import gauss
from pandas import Series
import networkx as net
import matplotlib.pyplot as plt
import cv2
import skimage


def image_noise(n):
    r = np.random.normal(0, 1, pow(n, 2))
    maxr = max(r)
    minr = min(r)
    rnorm = [255 * (i - minr) / (maxr - minr) for i in r]
    noise = [[rnorm[(j - 1) * n + i] for j in range(n)] for i in range(n)]
    return noise

def add_noise(image, noise, coeff):
    return np.clip([[z + coeff * (2 * w - 255) for (z, w) in zip(x, y)] for (x, y) in zip(image, noise)], 0, 255)

def degree_matrix(ivg: IVG):
    n = ivg.size
    G = ivg.nx
    return [[len(G[(i, j)]) for j in range(n)] for i in range(n)]

def clustering_matrix(ivg: IVG):
    n = ivg.size
    G = ivg.nx
    return [[net.clustering(G, (i, j)) for j in range(n)] for i in range(n)]

def and_matrix(ivg: IVG):
    n = ivg.size
    G = ivg.nx
    degs = degree_matrix(ivg)
    return [[np.mean([degs[k][l] for (k, l) in G[(i, j)]]) for j in range(n)] for i in range(n)]

def knn_matrix(ivg: IVG):
    n = ivg.size
    G = ivg.nx
    degs = degree_matrix(ivg)
    deg_seq = [x for xs in degs for x in xs]
    deg_vals = list(set(deg_seq))
    deg_dict = {deg: deg_seq.count(deg) for deg in deg_vals}
    ln = sum([sum(row) for row in degs])
    h = {(deg1, deg2): 0 for deg1 in deg_vals for deg2 in deg_vals}
    for edge in G.edges:
        h[degs[edge[0][0]][edge[0][1]], degs[edge[1][0]][edge[1][1]]] += 1
        h[degs[edge[1][0]][edge[1][1]], degs[edge[0][0]][edge[0][1]]] += 1
    h = {key: h[key] / ln for key in h}
    fstar = {k: k * deg_dict[k] / (ln * n ** 2) for k in deg_vals}
    knn_dict = {k: sum([j * h[k, j] for j in deg_vals]) / fstar[k] for k in deg_vals}
    return [[knn_dict[deg] for deg in row] for row in degs]

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
