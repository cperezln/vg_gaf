import numpy as np
import networkx as net

class HorizontalVisibilityGraph:
    __nx = None
    __datastructure = None

    def fillsFromTimeSeries(series):
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
        return HorizontalVisibilityGraph(matrix)
        
    def __init__(self, matrix):
        """
        Generate a horizontal visibility graph (HVG) adjacency matrix for a given time series.
        :param series: time series
        :return graph: adjacency matrix
        """
        self.__datastructure = matrix


    @property
    def matrix(self):
        return self.__datastructure

    @property
    def nx(self):
        if self.__nx == None:
            self.__nx = net.Graph(np.array(self.matrix))
        return self.__nx
    
    def to_np(self):
        return np.array(self.__datastructure)