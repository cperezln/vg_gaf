def hvg(series):
    n = len(series)
    graph = []
    matrix = [[] for _ in range(n)]
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
                matrix[[i, j]] = 1
    return graph, matrix