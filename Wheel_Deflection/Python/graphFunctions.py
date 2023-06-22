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

    smooth_mean = convolve(mean_of_displacements, np.ones(360) / 360, mode='valid')
    smooth_std = convolve(std_of_displacements, np.ones(360) / 360, mode='valid')

    pad = len(independent_variable) - len(smooth_mean)

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title(r'n=20 Shaded Region: +/- 1 $\sigma$')

    lower_bound = smooth_mean - smooth_std
    upper_bound = smooth_mean + smooth_std

    plt.fill_between(independent_variable[pad:], lower_bound, upper_bound, color='green', alpha=.1)
    plt.plot(independent_variable[pad:], smooth_mean, color='gray')

    plt.setp(plt.gca().lines, linewidth=1)

    # Individual test graph
    plt.subplot(122)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    plt.title('Individual test data n=20')

    for i in range(displacements.shape[0]):
        plt.plot(independent_variable, displacements[i], label=f'Test {i + 1}')

    # plt.legend()
    plt.show()


""""
Plot multiple shaded error bad graphs onto the same graph.
There is also functionality for having multiple of the same sets be the same color but as a dotted line.
For example if you have a set of "new_Enve" data and "old_Enve" data you can graph them as the same color but one 
will be a dotted line.
"""


def multiple_rims_graph(mean_list, std_list, ind_var, rims, old_data_index=0):
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
        # interpolated_mean = np.interp(unified_ind_var, ind_var[i], mean_list[i])
        # interpolated_std = np.interp(unified_ind_var, ind_var[i], std_list[i])
        smooth_mean = convolve(mean_list[i], np.ones(360) / 360, mode='valid')
        smooth_std = convolve(std_list[i], np.ones(360) / 360, mode='valid')

        pad = len(unified_ind_var) - len(smooth_mean)

        lower_bound = smooth_mean - smooth_std
        upper_bound = smooth_mean + smooth_std

        rim_label = rims[i]
        for color_key in color_mapping.keys():
            if color_key in rim_label:
                color = color_mapping[color_key]
                break
        else:
            color = mcolors.hsv_to_rgb((hues[i], 1, 1))  # Convert HSV to RGB
            color_mapping[rim_label] = color

        plt.fill_between(unified_ind_var[pad:], lower_bound, upper_bound, color=color, alpha=.1)

        if i >= old_data_index != 0:
            line_style = '--'
            label = rim_label.replace("old ", "")  # Remove "old " from the label
        else:
            line_style = '-'
            label = rim_label

        plt.plot(unified_ind_var[pad:], smooth_mean, color=color, linestyle=line_style, label=label)
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

    fig, axs = plt.subplots(num_plots, 1, figsize=(12, 3*num_plots), sharex=True)

    for i, (df, target) in enumerate(zip(df_list, targets)):
        left_tension = df['Left Tension (kgf)']
        right_tension = df['Right Tension (kgf)']

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

    plt.xlabel('Set')
    # plt.suptitle('Deviation from Target Tension After Each Set')
    # plt.title('n=5 for each set')

    plt.tight_layout()
    plt.show()