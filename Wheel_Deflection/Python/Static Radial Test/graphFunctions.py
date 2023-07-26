import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import linregress

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

    smooth_mean = convolve(mean_of_displacements, np.ones(360) / 360, mode='valid')
    smooth_std = convolve(std_of_displacements, np.ones(360) / 360, mode='valid')

    pad = len(independent_variable) - len(smooth_mean)

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title(r'n=20 Shaded Region: +/- 1 $\sigma$')

    lower_bound = smooth_mean - smooth_std
    upper_bound = smooth_mean + smooth_std

    plt.fill_between(independent_variable[pad:], lower_bound, upper_bound, color='green', alpha=.1)
    plt.plot(independent_variable[pad:], smooth_mean, color='gray', label='Data')

    plt.setp(plt.gca().lines, linewidth=1)
    #
    # Linear regression
    x = independent_variable[pad:]
    y = smooth_mean
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    # Plot regression line
    plt.plot(x, intercept + slope * x, color='red', label='Linear Regression', linestyle='dotted')
    print(intercept, slope)
    # # Polynomial regression
    # x = independent_variable[pad:]
    # y = smooth_mean
    # degree = 2 # Define the degree of the polynomial
    # coefficients = np.polyfit(x, y, degree)
    # poly = np.poly1d(coefficients)
    # print(coefficients, poly)
    #
    # # Plot regression line
    # equation = f'y = {coefficients[0]}x^2 + {coefficients[1]}x + {coefficients[2]}'
    # print(equation)
    #
    # plt.plot(x, poly(x), color='purple', label=f'Polynomial Regression', linestyle='dashed')
    # plt.legend()


    # Individual test graph
    plt.subplot(122)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    plt.title('Individual test data n=20')

    for i in range(displacements.shape[0]):
        plt.plot(independent_variable, displacements[i], label=f'Test {i + 1}')

    # plt.legend()
    ax.set_xlim(ax.get_xlim()[::-1])

    plt.show()


""""
Plot multiple shaded error bad graphs onto the same graph.
There is also functionality for having multiple of the same sets be the same color but as a dotted line.
For example if you have a set of "new_Enve" data and "old_Enve" data you can graph them as the same color but one 
will be a dotted line.
"""


def multiple_rims_graph(mean_list, std_list, ind_var, rims, old_data_index=0, smoothing_window=1500):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))

    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title(r'Shaded Region: +/- 1 $\sigma$   n=20')

    hues = np.linspace(0, 1, len(mean_list) + 1)  # Generate equally spaced hues

    unified_ind_var = np.unique(np.concatenate([ind_var[i] for i in range(len(ind_var))]))

    color_mapping = {}  # Store the mapping between rim labels and colors

    for i in range(len(mean_list)):
        interpolated_mean = np.interp(unified_ind_var, ind_var[i], mean_list[i])
        interpolated_std = np.interp(unified_ind_var, ind_var[i], std_list[i])

        smooth_std = smoothing(interpolated_std, smoothing_window)
        smooth_mean = smoothing(interpolated_mean, smoothing_window)

        lower_bound = smooth_mean - smooth_std
        upper_bound = smooth_mean + smooth_std

        if 'Stans' in rims[i] or 'DTS' in rims[i]:
            color = 'blue'
            label = 'Alloy'
        else:
            color = 'red'
            label = 'Carbon'
        # elif 'Stans' in rims[i] or 'WAOU' in rims[i]:
        #     color = 'red'
        #     label = '3-cross 32'
        # elif 'DTS' in rims[i] or 'R30' in rims[i]:
        #     color = 'green'
        #     label = '3-cross 28'
        # elif 'Light' in rims[i]:
        #     color = 'orange'
        #     label = '2-cross 32'
        rim_label = rims[i]
        # for color_key in color_mapping.keys():
        #     if color_key in rim_label:
        #         color = color_mapping[color_key]
        #         break
        # else:
        #     color = mcolors.hsv_to_rgb((hues[i], 1, 1))  # Convert HSV to RGB
        #     color_mapping[rim_label] = color

        plt.fill_between(unified_ind_var[smoothing_window - 1:], lower_bound, upper_bound, color=color, alpha=.1)
        plt.plot(unified_ind_var[smoothing_window - 1:], smooth_mean, color=color, label=label)

        plt.setp(plt.gca().lines, linewidth=1)

    plt.legend()
    plt.show()


def lateral_deviation_plot(df, tests):
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = .07
    group_offset = np.arange(tests) * bar_width

    for i in range(tests):
        tensions = df['Tension' + str(i+1)]
        x_positions = np.arange(len(df['Rim'])) + group_offset[i]
        ax.bar(x_positions, tensions, width=bar_width, label='Test Set {}'.format(i+1))

    ax.set_xticks(np.arange(len(df['Rim'])) + (tests - 1) * bar_width / 2)
    ax.set_xticklabels(df['Rim'])

    ax.set_ylabel('Lateral Deviation (mm)')
    plt.suptitle('Spoke Tensions After Each Test Set')
    plt.title('Target .2mm, n=5 per set')

    fig.legend(loc='upper left')
    plt.show()


def spoke_tension_plot(df_list, targets, rims):
    num_plots = len(df_list)
    num_cols = 2  # Number of columns in the grid

    # Calculate the number of rows needed based on the number of plots and columns
    num_rows = (num_plots + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 3*num_rows), sharex='all')

    # Flatten the axs array if it's not already flattened
    if axs.ndim > 1:
        axs = axs.flatten()

    for i, (df, target) in enumerate(zip(df_list, targets)):
        left_tension = df['Left Tension (kgf)']
        right_tension = df['Right Tension (kgf)']

        # Calculate the subplot position in the grid
        row = i // num_cols
        col = i % num_cols

        # Plot the left tension
        axs[i].plot(left_tension, 'bo-', label='Left Tension')
        axs[i].axhline(y=target, color='r', linestyle='--', label='Target Tension')
        axs[i].set_ylabel('Tension')

        # Plot the right tension
        axs[i].plot(right_tension, 'go-', label='Right Tension')
        axs[i].axhline(y=target, color='r', linestyle='--')
        axs[i].legend()

        # Set the subplot title as the rim name
        axs[i].set_title(rims[i])

    # Hide empty subplots if any
    if num_plots < num_rows * num_cols:
        for j in range(num_plots, num_rows * num_cols):
            axs[j].axis('off')

    plt.xlabel('Set')
    # plt.suptitle('Deviation from Target Tension After Each Set')
    # plt.title('n=5 for each set')

    plt.tight_layout()
    plt.show()


def smoothing(data, window_size):
    cumsum = np.cumsum(np.insert(data, 0, 0))
    return (cumsum[window_size:] - cumsum[:-window_size]) / float(window_size)