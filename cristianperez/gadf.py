import numpy as np
def gadf(series):
    m = min(series)
    M = max(series)
    rescaled = [(2*i - M - m)/(M - m) for i in series]
    angles = [np.arccos(i) for i in rescaled]
    g = [[np.sin(i) - np.sin(j) for i in angles] for j in angles]
    return g