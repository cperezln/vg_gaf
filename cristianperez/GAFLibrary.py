import numpy as np

def GramianSummationField(f = np.cos, series = [], I = [0, 1]):
    m = min(series)
    M = max(series)
    a, b = I
    rescaled = [a + (i - m)*(b-a)/(M - m) for i in series]
    angles = [np.arccos(i) for i in rescaled]
    g = np.array([[f(i + j) for j in angles] for i in angles])
    return g

def GramianDifferenceField(f = np.sin, series = [], I = [0, 1]):
    m = min(series)
    M = max(series)
    a, b = I
    rescaled = [a + (i - m)*(b-a)/(M - m) for i in series]
    angles = [np.arccos(i) for i in rescaled]
    g = np.array([[f(i - j) for j in angles] for i in angles])
    return g
