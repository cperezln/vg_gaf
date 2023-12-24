def vg(series):
    n = len(series)
    graph = []
    matrix = [[0]*100 for _ in range(n)]
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
    return graph, matrix