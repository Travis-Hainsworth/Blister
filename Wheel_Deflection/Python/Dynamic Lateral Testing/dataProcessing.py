import cProfile
from scipy.signal import find_peaks
from readInDataFiles import *


def data_processor(file_path):
    # pro = cProfile.Profile()
    # pro.enable()
    df, height, rim, head = get_mocap_data(file_path)
    list_mocap_data, displacements = clean_mocap_data(df)
    q_drop_heights = []
    q_percent_absorbed = []

    for i, df in enumerate(list_mocap_data):
        index_of_starting_height = df['drop_head_y'].argmax()
        displacements[i] = displacements[i] * .0393701

        starting_height = df['drop_head_y'][index_of_starting_height]
        height_of_rebound, _ = find_peaks(df['drop_head_y'], prominence=1)
        rebound_peak_heights = df['drop_head_y'].iloc[height_of_rebound]
        # regular drop heads
        # potential_energy = (starting_height/1000) * 9.8 * (46.705 * .4535)
        potential_energy = (starting_height/1000) * 9.8 * (45.3104 * .4535)

        try:
            height_diff = starting_height - rebound_peak_heights[0]
        except IndexError:
            pass

        potential_energy_2 = (height_diff/1000) * 9.8 * (46.705 * .4535)
        percent_absorbed = (potential_energy - potential_energy_2)

        q_drop_heights.append(int(height[i]))
        q_percent_absorbed.append(percent_absorbed)
    # pro.disable()
    # pro.print_stats(sort='cumtime')
    return q_percent_absorbed, displacements, q_drop_heights, rim, head


def file_processor(filepaths):
    energies, percents, heights, rims, heads = [], [], [], [], []
    for filepath in filepaths:
        energy, percent, height, rim, head = data_processor(filepath)
        energies.append(energy)
        heights.append(height)
        rims.append(rim)
        percents.append(percent)
        heads.append(head)

    return energies, percents, heights, rims, heads


def index_filtering(percent_diffs, x_axis):

    x_axis = np.array(x_axis).astype(float)
    percent_diffs = np.array(percent_diffs). astype(float)

    # Sort the data based on x_axis values
    sorted_indices = np.argsort(x_axis)
    sorted_x_axis = x_axis[sorted_indices]
    sorted_percent_diffs = percent_diffs[sorted_indices]

    return sorted_percent_diffs, sorted_x_axis



