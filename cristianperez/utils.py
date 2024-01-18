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


def draw_side_by_side(x, time_points, gasf, gadf, width=10):
    height = width * 9/16
    fig = plt.figure(figsize=(width, height))
    gs = fig.add_gridspec(2, 4, left=0.1, 
                        right=0.9, bottom=0.1, top=0.9,
                        wspace=0.1, hspace=0.1)

    # Define the ticks and their labels for both axes
    # time_ticks = np.linspace(0, 4 * np.pi, 9)
    # time_ticklabels = [r'$0$', r'$\frac{\pi}{2}$', r'$\pi$',
    #                 r'$\frac{3\pi}{2}$', r'$2\pi$', r'$\frac{5\pi}{2}$',
    #                 r'$3\pi$', r'$\frac{7\pi}{2}$', r'$4\pi$']
    value_ticks = [-1, 0, 1]
    reversed_value_ticks = value_ticks[::-1]

    # Plot the time series on the left with inverted axes
    ax_left = fig.add_subplot(gs[1, 0])
    ax_left.plot(x, time_points)
    ax_left.set_xticks(reversed_value_ticks)
    ax_left.set_xticklabels(reversed_value_ticks, rotation=90)
    # ax_left.set_yticks(time_ticks)
    # ax_left.set_yticklabels(time_ticklabels, rotation=90)
    # ax_left.set_ylim((0, 4 * np.pi))
    ax_left.invert_xaxis()

    # Plot the time series on the top
    ax_top1 = fig.add_subplot(gs[0, 1])
    ax_top2 = fig.add_subplot(gs[0, 2])
    for ax in (ax_top1, ax_top2):
        ax.plot(time_points, x)
        # ax.set_xticks(time_ticks)
        # ax.set_xticklabels(time_ticklabels)
        ax.set_yticks(value_ticks)
        ax.xaxis.tick_top()
        # ax.set_xlim((0, 4 * np.pi))
    ax_top1.set_yticklabels(value_ticks)
    ax_top2.set_yticklabels([])

    # Plot the Gramian angular fields on the bottom right
    ax_gasf = fig.add_subplot(gs[1, 1])
    ax_gasf.imshow(gasf, cmap='rainbow', origin='lower')
    # ax_gasf.imshow(gasf, cmap='rainbow', origin='lower',
    #             extent=[0, 4 * np.pi, 0, 4 * np.pi])
    ax_gasf.set_xticks([])
    ax_gasf.set_yticks([])
    ax_gasf.set_title('Gramian Angular Summation Field', y=-0.09)

    ax_gadf = fig.add_subplot(gs[1, 2])
    im = ax_gadf.imshow(gadf, cmap='rainbow', origin='lower')
    # im = ax_gadf.imshow(gadf, cmap='rainbow', origin='lower',
    #                     extent=[0, 4 * np.pi, 0, 4 * np.pi])
    ax_gadf.set_xticks([])
    ax_gadf.set_yticks([])
    ax_gadf.set_title('Gramian Angular Difference Field', y=-0.09)

    # Add colorbar
    ax_cbar = fig.add_subplot(gs[1, 3])
    fig.colorbar(im, cax=ax_cbar)

    plt.show()
