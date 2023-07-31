import re
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema
from scipy.spatial.transform import Rotation
import numpy as np
from scipy import signal
from readInDataFiles import *


def process_field_data(list_df):
    all_wheel_quat = []
    all_hub_quat = []
    wheel_cords = []
    hub_cords = []
    Rs = []

    for df in list_df:
        # Finds the index where the wheel fully enters the frames
        start_index = df[df[' X'].astype(float) > 0].index[0]
        current_value = df[' X'].iloc[int(start_index) + 100]
        end_index = int(start_index) + 250
        print(start_index)

        for h in range(int(start_index) + 1, len(df)):
            if df[' X'].iloc[h] == current_value:
                end_index = h
            else:
                break
        df = df.iloc[int(start_index):int(end_index) + 1]

        print(list(df.columns))

        # Remove nan columns
        df = df.dropna(how='all')
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)

        # Convert columns to numeric values
        column_names_to_convert = [' X', 'Hub.1 Y', 'Hub.1 Z', 'Hub.1 W', 'Wheel X', 'Wheel Y', 'Wheel Z', 'Wheel.3 W']
        # column_names_to_convert = ['Hub X', 'Hub Y', 'Hub Z', 'Hub.3 W', ' X', 'Wheel.1 Y', 'Wheel.1 Z', 'Wheel.1 W']

        converted_columns = convert_to_numeric(df, column_names_to_convert)
        x_rot_hub, y_rot_hub, z_rot_hub, w_hub, x_rot_wheel, y_rot_wheel, z_rot_wheel, w_rot_wheel = converted_columns

        # Find quaternion of the hub and wheel
        hub_quat = np.column_stack((x_rot_hub, y_rot_hub, z_rot_hub, w_hub))
        wheel_quat = np.column_stack((x_rot_wheel, y_rot_wheel, z_rot_wheel, w_rot_wheel))
        all_wheel_quat.append(wheel_quat)
        all_hub_quat.append(hub_quat)

        # Find every coordinate column for the hub and the wheel
        all_wheel_y, all_hub_y = process_wheel_hub(df, wheel_pattern_y, hub_pattern_y)
        all_wheel_x, all_hub_x = process_wheel_hub(df, wheel_pattern_x, hub_pattern_x)
        all_wheel_z, all_hub_z = process_wheel_hub(df, wheel_pattern_z, hub_pattern_z)
        all_quats = []

        for i in range(len(all_wheel_y[0])):
            quat_diff = hub_quat[i] * wheel_quat[i]
            all_quats.append(quat_diff)

        for i in range(len(all_wheel_y)):
            for j in range(len(all_wheel_y[i])):
                # # Rotation stuff
                r = Rotation.from_quat(all_quats[i])
                R = r.as_matrix()

                wheel_cord = list(zip(all_wheel_x[i].tolist(), all_wheel_y[i].tolist(), all_wheel_z[i].tolist()))
                hub_cord = list(zip(all_hub_x[0], all_hub_y[0], all_hub_z[0]))

                wheel_cords.append(wheel_cord)
                hub_cords.append(hub_cord)
                Rs.append(R)

        all_mags = []
        for i in range(len(wheel_cords)):
            mags_per_marker = set()
            for j in range(len(wheel_cords[i])):
                result = tuple(x - y for x, y in zip(wheel_cords[i][j], hub_cords[i][j]))
                vector = Rs[i] @ result
                if vector[2] < 0:
                    rotated_displacement_magnitudes = np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
                    mags_per_marker.add(rotated_displacement_magnitudes)

            if mags_per_marker not in all_mags:
                all_mags.append(mags_per_marker)

        for i, mags in enumerate(all_mags):
            list_mags = remove_outliers(list(mags), threshold=.6)
            arr_mags = np.asarray(list_mags)

            x_values = range(len(list_mags))
            coef = np.polyfit(x_values, list_mags, 15)
            trend_line = np.polyval(coef, x_values)

            data = list_mags - trend_line
            data_smaller_peaks = shrink_peaks(abs(data), .3)
            detrend = signal.detrend(abs(data_smaller_peaks))
            mean = np.mean(detrend)
            std = np.std(detrend)

            if std < 1:
                print(f"mean {mean}, std {std}")
                plt.plot(range(len(detrend)), abs(detrend), label=f'Set {i + 1}')

        plt.xlabel('Frame')
        plt.ylabel('abs(Magnitude) (mm)')
        plt.title('Magnitude Distribution for Each Set of Markers')
        plt.legend()
        plt.grid(True)
        plt.show()
        # 141


# Helper Function
def normalize_data(data):
    mean_data = np.mean(data)
    std_data = np.std(data)
    normalized_data = (data - mean_data) / std_data
    return normalized_data


# Helper Function
def shrink_peaks(data, shrink_factor):
    peak_indices = argrelextrema(data, np.greater)
    for peak_index in peak_indices:
        data[peak_index] *= shrink_factor

    return data


# Helper function
def remove_duplicates_preserve_order(input_list):
    unique_elements = {}
    result_list = []

    for item in input_list:
        if item not in unique_elements:
            unique_elements[item] = True
            result_list.append(item)

    return result_list


# Helper function
def process_wheel_hub(df, wheel_pattern, hub_pattern):
    wheel_cols = [col for col in df.columns if re.match(wheel_pattern, col)]
    hub_cols = [col for col in df.columns if re.match(hub_pattern, col)]
    all_wheel = []
    all_hub = []

    for wheel in wheel_cols:
        wheel_values = pd.to_numeric(df[wheel], errors='coerce').dropna()
        all_wheel.append(wheel_values)

    for hub in hub_cols:
        hub_values = pd.to_numeric(df[hub], errors='coerce').dropna()
        all_hub.append(hub_values)

    return all_wheel[:26], all_hub[:5]


# Helper function
def convert_to_numeric(df, column_names):
    converted_columns = []
    for col in column_names:
        converted_col = pd.to_numeric(df[col], errors='coerce')
        converted_columns.append(converted_col)

    return converted_columns


def remove_outliers(data, threshold=1):
    data = np.array(data)
    mean_val = np.mean(data)
    std_val = np.std(data)
    z_scores = np.abs((data - mean_val) / std_val)
    # Remove values that have a Z-score greater than the threshold
    filtered_data = data[z_scores <= threshold]

    return filtered_data.tolist()


def data_processor(file_path):
    df, rim = get_mocap_data(file_path)
    process_field_data(df)


# def rodrigues_rotation(angle, axis):
#     # Angle in radians
#     k = axis / np.linalg.norm(axis)
#     K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
#     R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
#     return R