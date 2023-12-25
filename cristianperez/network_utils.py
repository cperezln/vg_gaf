import itertools

import networkx as nx
from networkx import sigma
from random import gauss
import numpy as np
from matplotlib import pyplot as plt
from pandas import Series

def white_noise(n):
    ts = [gauss(0, 1) for i in range(n)]
    return Series(ts)

def horizontal_visibility_graph(series):
    """
    Return a Visibility Graph of an input Time Series.

    A visibility graph converts a time series into a graph. The constructed graph
    uses integer nodes to indicate which event in the series the node represents.
    Edges are formed as follows: consider a bar plot of the series and view that
    as a side view of a landscape with a node at the top of each bar. An edge
    means that the nodes can be connected by a straight "line-of-sight" without
    being obscured by any bars between the nodes.

    The resulting graph inherits several properties of the series in its structure.
    Thereby, periodic series convert into regular graphs, random series convert
    into random graphs, and fractal series convert into scale-free networks [1]_.

    Parameters
    ----------
    series : Sequence[Number]
       A Time Series sequence (iterable and sliceable) of numeric values
       representing times.

    Returns
    -------
    NetworkX Graph
        The Visibility Graph of the input series

    Examples
    --------
    >>> series_list = [range(10), [2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3]]º
    >>> for s in series_list:
    ...     g = nx.visibility_graph(s)
    ...     print(g)
    Graph with 10 nodes and 9 edges
    Graph with 12 nodes and 18 edges

    References
    ----------
    .. [1] Lacasa, Lucas, Bartolo Luque, Fernando Ballesteros, Jordi Luque, and Juan Carlos Nuno.
           "From time series to complex networks: The visibility graph." Proceedings of the
           National Academy of Sciences 105, no. 13 (2008): 4972-4975.
           https://www.pnas.org/doi/10.1073/pnas.0709247105
    """

    # Sequential values are always connected
    G = nx.path_graph(len(series))
    nx.set_node_attributes(G, dict(enumerate(series)), "value")

    # Check all combinations of nodes n series
    for (n1, t1), (n2, t2) in itertools.combinations(enumerate(series), 2):

        obstructed = any(
            t >= min(t1, t2)
            for n, t in enumerate(series[n1 + 1 : n2], start=n1 + 1)
        )

        if not obstructed:
            G.add_edge(n1, n2)

    return G
# Press the green button in the gutter to run the script.
def plot_hist(instances, nodes, vg = True, hvg = True):
    time_series = [white_noise(10000) for i in range(instances)]

    time_series_used = [ts[:nodes] for ts in time_series]
    degreesG = []
    degreesHG = []
    if vg:
        lsG = [nx.visibility_graph(i) for i in time_series_used]
        degreesG = [[d for n, d in g.degree()] for g in lsG]
        degreesG = [item for row in degreesG for item in row]
        counts1, bins1 = np.histogram(degreesG)
        plt.hist(bins1[:-1], bins1, weights=counts1, label="Visibility Graph", alpha=.3, color="red")
    if hvg:
        lsHG = [horizontal_visibility_graph(i) for i in time_series_used]
        degreesHG = [[d for n, d in g.degree()] for g in lsHG]
        degreesHG = [item for row in degreesHG for item in row]
        counts2, bins2 = np.histogram(degreesHG)
        plt.hist(bins2[:-1], bins2, weights=counts2, label="Horizontal Visibility Graph", alpha=.3, color="green")
    plt.legend()
    plt.show()
    return (degreesG, degreesHG), (lsG, lsHG), time_series,
