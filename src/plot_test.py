import matplotlib.pyplot as plt
import pickle
import numpy as np
import argparse
from itertools import product


OBJECT_DISTANCE = 1
VERGENCE_ERROR = 2


def get_new_ax(fig, n_subplots, subplot_index, methode="square"):
    if methode == "square":
        n = int(np.ceil(np.sqrt(n_subplots)))
        if n != np.sqrt(n_subplots):
            m = n + 1
        else:
            m = n
        return fig.add_subplot(m, n, subplot_index + 1)
    if methode == "horizontal":
        return fig.add_subplot(1, n_subplots, subplot_index + 1)
    if methode == "vertical":
        return fig.add_subplot(n_subplots, 1, subplot_index + 1)


def filter_data(data, stimulus=None, object_distances=None, vergence_errors=None, speed_errors=None, n_iterations=None):
    test_cases = np.array([a for a, b in data])
    condition = np.ones_like(test_cases, dtype=np.bool)
    if stimulus is not None:
        condition = np.logical_and(condition, np.isin(test_cases["stimulus"], stimulus))
    if object_distances is not None:
        condition = np.logical_and(condition, np.isin(test_cases["object_distance"], object_distances))
    if vergence_errors is not None:
        condition = np.logical_and(condition, np.isin(test_cases["vergence_error"], vergence_errors))
    if speed_errors is not None:
        speed_errors = np.array(speed_errors, dtype=np.float32).view(dtype='f,f')
        speed_errors2 = np.ascontiguousarray(test_cases["speed_error"].reshape((-1,))).view(dtype='f,f')
        condition = np.logical_and(condition, np.isin(speed_errors2, speed_errors))
    return [data_point for data_point, pred in zip(data, condition) if pred]


def plot_vergence_trajectory_all(fig, lists_of_param_anchors, data):
    # generate sub lists of param anchors
    data = filter_data(data, **lists_of_param_anchors)
    list_of_subdata = [filter_data(data, object_distances=[d]) for d in lists_of_param_anchors["object_distances"]]
    n_subplots = len(lists_of_param_anchors["object_distances"])
    # for each sublist, plot in an ax
    for subplot_index, subdata in enumerate(list_of_subdata):
        ax = get_new_ax(fig, n_subplots, subplot_index, methode="horizontal")
        plot_vergence_trajectory_sub(ax, subdata)


def plot_vergence_trajectory_sub(ax, data):
    test_cases = np.array([a for a, b in data])
    for vergence_error in np.unique(test_cases["vergence_error"]):
        filtered = filter_data(data, vergence_errors=[vergence_error])
        # plot for each stimulus in light grey
        test_data = np.array([b for a, b in filtered])
        ax.plot(test_data["vergence_error"].T, color="grey", alpha=0.2)
        # plot mean and std
        ax.plot(np.mean(test_data["vergence_error"].T, axis=1))
        # plot a little horizontal line to indicate where the vergence error starts
        ax.axhline(y=vergence_error, xmin=0, xmax=1, color="r")
    # plot the abscissa, add title, axis label etc...
    ax.axhline(0, color="k")


if __name__ == "__main__":
    fig = plt.figure()

    with open("../test_conf/vergence_trajectory_4_distances.pkl", "rb") as f:
        lists_of_param_anchors = pickle.load(f)["test_descriptions"]["vergence_trajectory"]

    with open("../tmp/3134260_3.pkl", "rb") as f:
        data = pickle.load(f)

    plot_vergence_trajectory_all(fig, lists_of_param_anchors, data)
    plt.show()