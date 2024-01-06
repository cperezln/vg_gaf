import numpy as np
def gasf(series):
    m = min(series)
    M = max(series)
    rescaled = [(2*i - M - m)/(M - m) for i in series]
    angles = [np.arccos(i) for i in rescaled]
    g = [[np.cos(i + j) for i in angles] for j in angles]
    return g