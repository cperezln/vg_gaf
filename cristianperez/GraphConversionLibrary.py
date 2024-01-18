# From time series to graphs using Visibility Graphs
def hvg(series):
    n = len(series)
    graph = []
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            flag = True
            m = min(series[i], series[j])
            for k in range(i + 1, j):
                if series[k] >= m:
                    flag = False
                    break
            if flag == True:
                graph.append((i,j))
                matrix[i][j] = 1
                matrix[j][i] = 1
    return graph, matrix

def vg(series):
    n = len(series)
    graph = []
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            flag = True
            for k in range(i + 1, j):
                if series[k] >= series[i] + (k - i) / (j - i) * (series[j] - series[i]):
                    flag = False
                    break
            if flag == True:
                graph.append((i,j))
                matrix[i][j] = (series[j] - series[i])/(j - i)
                matrix[j][i] = (series[i] - series[j])/(i - j)
    return graph, matrix

# From Gramian Angular Fields to Graphs 

def df_projection(m):
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
    return rm

def similarity_graph(gadcf, factor = 10, th = 0.96):
    ln = len(gacdf)
    g = [[0]*ln for i in range(ln)]
    for i in range(ln - 1):
        h = -2
        for j in range(i + 1, ln):
            if gacdf[i][j] > th:
                g[i][j] = factor*abs(i - j)
                g[j][i] = g[i][j]
    return g
