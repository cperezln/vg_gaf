class HorizontalVisibilityGraph:
    def __init__(self, series):
        """
        Generate a horizontal visibility graph (HVG) adjacency matrix for a given time series.
        :param series: time series
        :return graph: adjacency matrix
        """
        n = len(series)
        matrix = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                flag = True
                m = min(series[i],series[j])
                for k in range(i + 1, j):
                    if series[k] >= m:
                        flag = False
                        break
                if flag == True:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        self.__datastructure = matrix
    @property
    def matrix():
        return self.__datastructure