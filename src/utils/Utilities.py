from ..gramian.gramian import GramianAngularField
from ..visibility.horizontal.hvg import HorizontalVisibilityGraph
import numpy as np

def GramianProjection(GAF: GramianAngularField):
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

