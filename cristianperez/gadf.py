import numpy as np
def gadf(series, I = [-1, 1]):
    m = min(series)
    M = max(series)
    a, b = I
    rescaled = [a + (i - m)*(b-a)/(M - m) for i in series]
    angles = [np.arccos(i) for i in rescaled]
    g = np.array([[np.sin(i - j) for j in angles] for i in angles])
    #   g[(g < 1.22*10**-6) & (g > 0) | (g > -1.22*10**-6) & (g < 0)] = 0
    return g