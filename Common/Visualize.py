import numpy as np
import matplotlib.pyplot as plt


def plot_cycle(xs, ys, cycle, color):
    plt.scatter(np.array(xs)[cycle], np.array(ys)[cycle], c=color)
    for idx in range(len(cycle)):
        if idx+1 < len(cycle):
            plt.plot([xs[cycle[idx]], xs[cycle[idx+1]]], [ys[cycle[idx]], ys[cycle[idx+1]]], color)
        else:
            plt.plot([xs[cycle[idx]], xs[cycle[0]]], [ys[cycle[idx]], ys[cycle[0]]], color)


def plot_results(xs, ys, cycle_1, cycle_2,title=None):
    plt.rcParams["figure.figsize"] = (20, 15)
    plot_cycle(xs, ys, cycle_1, 'r')
    plot_cycle(xs, ys, cycle_2, 'b')
    if not(title is None):plt.title(title)
    plt.show()
