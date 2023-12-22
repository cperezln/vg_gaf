import numpy

def vg(series):
    n = len(series)
    graph = []
    for i in range(n):
        for j in range(i + 1, n):
            flag = True
            for k in range(i + 1, j):
                if series[k] >= series[i] + (k - i) / (j - i) * (series[j] - series[i]):
                    flag = False
                    break
            if flag == True:
                graph.append((i,j))
    return graph

def hvg(series):
    n = len(series)
    graph = []
    for i in range(n):
        for j in range(i + 1, n):
            flag = True
            m = min(series[i],series[j])
            for k in range(i + 1, j):
                if series[k] >= m:
                    flag = False
                    break
            #if any(list(map(lambda x : x >= m,series[i+1:j]))):
            if flag == True:
                graph.append((i,j))
    return graph

def gaf(series):
    m = min(series)
    M = max(series)
    f = lambda x : 2 * (x - m) / (M - m) - 1
    rescaled = list(map(f, series))
    angles = list(map(numpy.arccos, rescaled))
    g = list(map(lambda x : list(map(lambda y : numpy.cos(x + y), angles)), angles))
    return g
