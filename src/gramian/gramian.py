import numpy as np

class GramianAngularField:

    def __init__(self, op = 'dif', trig = np.sin, series = [], I = [0, 1]):
        """
        Generates an angular field, for a given operator (dif or sum), for a given trigonometric function.
        :param op: operator of the field (pred dif)
        :param f: function (pred np.sen)
        :param series: time series to compute the gramian angular field
        :param I: interval of normalization of the time series
        :return: matricial representation of the gramian angular field
        """
        op_allowed = ('dif', 'sum')
        f_allowed = (np.sin, np.cos)
        if op not in op_allowed or trig not in f_allowed:
            raise ValueError("Not allowed params. Operation must be summation ('sum') or difference ('dif'). Trigonometric function \
                must be np.sen or np.cos")
        self.__op = op
        self.__trig = trig
        m = min(series)
        M = max(series)
        a, b = I
        rescaled = [a + (i - m)*(b-a)/(M - m) for i in series]
        angles = [np.arccos(i) for i in rescaled]
        g = np.array([[trig(i - j) if op == 'dif' else trig(i + j) for j in angles] for i in angles])
        self.__datastructure = g
        
    @property
    def matrix(self):
        return self.__datastructure

    @property
    def op_type(self):
        return self.__op

    @property
    def function(self):
        return self.__trig
    
    def to_np(self):
        return np.array(self.__datastructure)
        