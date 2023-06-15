import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from dataProcessing import *
"""
PLots a shaded error bar graph of all tests performed. Shaded region is +/- 1 standard deviation.
Also plots the individual tests.
All the inputs come from the interpolate_data function.
"""


def plot_interpolated_data(displacements, mean_of_displacements, std_of_displacements, independent_variable):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))

    # Shaded error graph
    plt.subplot(121)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    lower_bound = mean_of_displacements - std_of_displacements
    upper_bound = mean_of_displacements + std_of_displacements

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title('Shaded Region: +/- 1 sigma')

    plt.fill_between(independent_variable, lower_bound, upper_bound, color='green', alpha=.15)
    plt.plot(independent_variable, mean_of_displacements, color='gray')

    plt.setp(plt.gca().lines, linewidth=1)

    # Individual test graph
    plt.subplot(122)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    plt.title('Individual test data')

    for i in range(displacements.shape[0]):
        plt.plot(independent_variable, displacements[i])

    plt.show()


def random_graphing(df_list):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    for i in range(len(df_list)):
        plt.plot(df_list[i]['Load (lbf)'], df_list[i]['Compression (in)'], color='gray')
    plt.show()


""""
Plot multiple shaded error bad graphs onto the same graph.
"""


def multiple_rims_graph(mean_list, std_list, ind_var, rims):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))

    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title('Shaded Region: +/- 2 sigma')

    hues = np.linspace(0, 1, len(mean_list)+1)[:-1]  # Generate equally spaced hues

    unified_ind_var = np.unique(np.concatenate([ind_var[i] for i in range(len(ind_var))]))

    for i in range(len(mean_list)):
        interpolated_mean = np.interp(unified_ind_var, ind_var[i], mean_list[i])
        interpolated_std = np.interp(unified_ind_var, ind_var[i], std_list[i])

        lower_bound = interpolated_mean - (2*interpolated_std)
        upper_bound = interpolated_mean + (2*interpolated_std)

        color = mcolors.hsv_to_rgb((hues[i], 1, 1))  # Convert HSV to RGB

        plt.fill_between(unified_ind_var, lower_bound, upper_bound, color=color, alpha=.3,
                         label=rims[i])
        plt.plot(unified_ind_var, interpolated_mean, color=color)

        plt.setp(plt.gca().lines, linewidth=1)

    plt.legend()
    plt.show()


