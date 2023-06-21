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
        plt.plot(independent_variable, displacements[i], label=f'Test {i + 1}')

    plt.legend()
    plt.show()


""""
Plot multiple shaded error bad graphs onto the same graph.
"""


def multiple_rims_graph(mean_list, std_list, ind_var, rims, old_data_index=0):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))

    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title(r'Shaded Region: +/- 1 $\sigma$   n=5')

    hues = np.linspace(0, 1, len(mean_list) + 1)  # Generate equally spaced hues

    unified_ind_var = np.unique(np.concatenate([ind_var[i] for i in range(len(ind_var))]))

    color_mapping = {}  # Store the mapping between rim labels and colors

    for i in range(len(mean_list)):
        interpolated_mean = np.interp(unified_ind_var, ind_var[i], mean_list[i])
        interpolated_std = np.interp(unified_ind_var, ind_var[i], std_list[i])

        lower_bound = interpolated_mean - interpolated_std
        upper_bound = interpolated_mean + interpolated_std

        rim_label = rims[i]
        for color_key in color_mapping.keys():
            if color_key in rim_label:
                color = color_mapping[color_key]
                break
        else:
            color = mcolors.hsv_to_rgb((hues[i], 1, 1))  # Convert HSV to RGB
            color_mapping[rim_label] = color

        plt.fill_between(unified_ind_var, lower_bound, upper_bound, color=color, alpha=.1)

        if i >= old_data_index != 0:
            line_style = '--'
            label = rim_label.replace("old ", "")  # Remove "old " from the label
        else:
            line_style = '-'
            label = rim_label

        plt.plot(unified_ind_var, interpolated_mean, color=color, linestyle=line_style, label=label)
        plt.setp(plt.gca().lines, linewidth=1)

    plt.legend()
    plt.show()


def spoke_tension_plot(compression, before, after):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['red', 'blue', 'green', 'black', 'yellow']

    plt.ylabel('Compression (in)')
    plt.xlabel('Lateral Deviation (in)')
    plt.scatter(before, compression, c=colors)
    plt.scatter(after, compression, c=colors, marker="x")
    plt.xticks(np.arange(0.005, .015, .005))

    plt.show()

