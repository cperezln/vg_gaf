import numpy as np
from sklearn.preprocessing import MinMaxScaler


def example_series(n_series: int, time: int) -> (np.array, np.array):
    """
    Generates a series of n_series in time steps.
    time >= 2 size for simplicity
    :param n_series: number of values of each series
    :param time: number of values in the final sample
    :return: values, period
    """
    period = time // n_series
    values = np.array(list(range(period)) * n_series)
    return values, period


class GAF:

    def __init__(self, x: np.array, threshold: float = 0):
        self.data = np.reshape(x, (-1, 1))
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled = scaler.fit_transform(self.data)
        vector_arccos = np.vectorize(np.arccos)
        angles = vector_arccos(self.scaled)
        vector_threshold = np.vectorize(lambda alpha: 0. if alpha < threshold else alpha)
        self.angles = vector_threshold(angles)

    def gasf(self):
        return np.array(
            [np.array([np.cos(x_i + x_j) for x_i in self.angles]) for x_j in self.angles]
        ).reshape((len(self.data), len(self.data)))

    def gadf(self):
        return np.array(
            [np.array([np.sin(x_i - x_j) for x_i in self.angles]) for x_j in self.angles]
        ).reshape((len(self.data), len(self.data)))
