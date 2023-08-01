import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def plot_lateral_deformations(mocap_datasets, mts_datasets, rims):
    fig, ax = plt.subplots()

    plt.ylabel('Lateral Deformation (mm)', fontsize=14)
    plt.xlabel('Load (lbf)', fontsize=14)

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires', fontsize=20)
    plt.title(r'Shaded Region: +/- 1 $\sigma$   n=25', fontsize=15)

    hues = np.linspace(0, 1, len(mocap_datasets) + 1)  # Generate equally spaced hues
    color_mapping = {}

    for i, (mocap, mts) in enumerate(zip(mocap_datasets, mts_datasets)):
        all_lines = []

        for j in range(len(mocap)):
            # Convert 'time' column in mocap to timedelta
            mocap[j]['Time (sec)'] = pd.to_timedelta(mocap[j]['Time (sec)'].astype(float), unit='s')

            # Resample mocap data to match the time points of mts data
            resampled_mocap = mocap[j].set_index('Time (sec)').resample('1s').mean()

            # Interpolate 'Load (lbf)' to match the time points of resampled mocap data
            interp_load = np.interp(
                np.linspace(0, 200, num=200),
                mts[j]['Time (sec)'].astype(float),
                mts[j]['Load (lbf)'].astype(float),
            )

            # Store individual line
            line = np.linspace(resampled_mocap['rim_y'].iloc[0], max(resampled_mocap['rim_y']), len(interp_load))
            all_lines.append(line)

        # Calculate the mean line and the padded lines for the current dataset
        max_len = max(len(line) for line in all_lines)

        all_lines_padded = [line.tolist() + [line[-1]] * (max_len - len(line)) for line in all_lines]

        mean_line = np.mean(all_lines_padded, axis=0)
        std_dev_line = np.std(all_lines_padded, axis=0)

        rim_label = rims[i]
        for color_key in color_mapping.keys():
            if color_key in rim_label:
                color = color_mapping[color_key]
                break
        else:
            color = mcolors.hsv_to_rgb((hues[i], 1, 1))  # Convert HSV to RGB
            color_mapping[rim_label] = color

        # Plot the mean line and the shaded error bar for the current dataset
        ax.plot(np.arange(len(mean_line)), mean_line, label=rims[i], color=color)
        ax.fill_between(np.arange(len(mean_line)), mean_line - (2 * std_dev_line), mean_line + (2 * std_dev_line),
                        color=color, alpha=0.2)

    ax.set_xlim([0, 200])
    ax.legend(fontsize=14)

    plt.show()

