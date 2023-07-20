import math
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
import os
import re
from matplotlib import pyplot as plt
from scipy.spatial.transform import Rotation
from dtypes import dtype_dict
import multiprocessing
import cProfile

NUM_CORES = multiprocessing.cpu_count()


def process_single_file(folder_dir, file):
    path = os.path.join(folder_dir, file.title())
    df = pd.read_csv(path, header=2, low_memory=False, dtype=dtype_dict)

    file_parts = str(path).split('_')
    rim = file_parts[2]

    df = df.drop(index=[0, 1])
    df = fix_mocap_df(df)
    df = df.drop(index=2)
    df.set_index('Frame', inplace=True)

    return df, rim


# Function to process all CSV files in a folder using parallel processing
def get_mocap_data(folder_dir):
    files = sorted(os.listdir(folder_dir))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=NUM_CORES) as executor:
        processed_data = list(executor.map(process_single_file, [folder_dir] * len(files), files))

    # Unpack the results into separate lists
    combined_csvs, rim = zip(*processed_data)
    return combined_csvs, rim


def fix_mocap_df(df):
    new_cols = {'Unnamed: 0': 'Frame', 'Name': 'Time (sec)'}
    first_row = df.iloc[0]
    marker_name = ""

    for count, col in enumerate(df.columns):
        if count >= 2:
            if count % 3 == 0:
                marker_name = col
            new_cols[col] = marker_name + " " + first_row[count]

    df = df.rename(columns=new_cols, errors="raise")
    return df


def clean_mocap_data(list_df):
    clean_list_df = []
    max_list = []
    disp_x, disp_y, disp_z, disp = [], [], [], []
    all_wheel_y, all_wheel_x, all_wheel_z = [], [], []
    all_hub_x, all_hub_y, all_hub_z = [], [], []
    wheel_pattern_y = r'^Wheel:Marker\d+\.\d+ Y$'
    hub_pattern_y = r'^Hub:Marker\d+\.\d+ Y$'
    wheel_pattern_x = r'^Wheel:Marker\d+\.\d+ X$'
    hub_pattern_x = r'^Hub:Marker\d+\.\d+ X$'
    wheel_pattern_z = r'^Wheel:Marker\d+\.\d+ Z$'
    hub_pattern_z = r'^Hub:Marker\d+\.\d+ Z$'
    all_wheel_quat = []
    all_hub_quat = []

    for df in list_df:
        start_index = df[df[' X'].astype(float) > 0].index[0]
        print(df.columns.tolist())

        df = df.iloc[int(start_index):]

        df = df.dropna(how='all')  # Assign the result back to df
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        x_rot_hub = pd.to_numeric(df['Hub X'], errors='coerce')
        y_rot_hub = pd.to_numeric(df['Hub Y'], errors='coerce')
        z_rot_hub = pd.to_numeric(df['Hub Z'], errors='coerce')
        w_hub = pd.to_numeric(df['Hub.3 W'], errors='coerce')

        x_rot_wheel = pd.to_numeric(df[' X'], errors='coerce')
        y_rot_wheel = pd.to_numeric(df['Wheel.1 Y'], errors='coerce')
        z_rot_wheel = pd.to_numeric(df['Wheel.1 Z'], errors='coerce')
        w_rot_wheel = pd.to_numeric(df['Wheel.1 W'], errors='coerce')

        hub_quat = np.column_stack((x_rot_hub, y_rot_hub, z_rot_hub, w_hub))
        wheel_quat = np.column_stack((x_rot_wheel, y_rot_wheel, z_rot_wheel, w_rot_wheel))
        all_wheel_quat.append(wheel_quat)
        all_hub_quat.append(hub_quat)

        wheel_col_y = [col for col in df.columns if re.match(wheel_pattern_y, col)]
        hub_col_y = [col for col in df.columns if re.match(hub_pattern_y, col)]

        wheel_col_x = [col for col in df.columns if re.match(wheel_pattern_x, col)]
        hub_col_x = [col for col in df.columns if re.match(hub_pattern_x, col)]

        wheel_col_z = [col for col in df.columns if re.match(wheel_pattern_z, col)]
        hub_col_z = [col for col in df.columns if re.match(hub_pattern_z, col)]

        for wheel in wheel_col_y:
            wheel_values_y = pd.to_numeric(df[wheel], errors='coerce')
            wheel_values_y = wheel_values_y.dropna()
            all_wheel_y.append(wheel_values_y)

        for hub in hub_col_y:
            hub_values_y = pd.to_numeric(df[hub], errors='coerce')
            hub_values_y = hub_values_y.dropna()
            all_hub_y.append(hub_values_y)

        for wheel in wheel_col_x:
            wheel_values_x = pd.to_numeric(df[wheel], errors='coerce')
            wheel_values_x = wheel_values_x.dropna()
            all_wheel_x.append(wheel_values_x)

        for hub in hub_col_x:
            hub_values_x = pd.to_numeric(df[hub], errors='coerce')
            hub_values_x = hub_values_x.dropna()
            all_hub_x.append(hub_values_x)

        for wheel in wheel_col_z:
            wheel_values_z = pd.to_numeric(df[wheel], errors='coerce')
            wheel_values_z = wheel_values_z.dropna()
            all_wheel_z.append(wheel_values_z)

        for hub in hub_col_z:
            hub_values_z = pd.to_numeric(df[hub], errors='coerce')
            hub_values_z = hub_values_z.dropna()
            all_hub_z.append(hub_values_z)

        for i in range(len(all_hub_y)):
            # Beats me
            quat_diff = all_hub_quat[0][i] * np.conj(all_wheel_quat[0][i])

            # Rotation stuff
            r = Rotation.from_quat(quat_diff)
            rotation_vector = r.as_rotvec()
            angle = np.linalg.norm(rotation_vector)
            axis = rotation_vector / angle
            R = r.as_matrix()

            # Conversion stuff
            angle_deg = np.degrees(angle)
            angle_rad = np.radians(angle_deg)

            disp_x_rot = R[0, 0] * (all_hub_x[i] - all_wheel_x[i]) + R[0, 1] * (all_hub_y[i] - all_wheel_y[i]) + R[
                0, 2] * (all_hub_z[i] - all_wheel_z[i])

            disp_y_rot = R[1, 0] * (all_hub_x[i] - all_wheel_x[i]) + R[1, 1] * (all_hub_y[i] - all_wheel_y[i]) + R[
                1, 2] * (all_hub_z[i] - all_wheel_z[i])
            disp_z_rot = R[2, 0] * (all_hub_x[i] - all_wheel_x[i]) + R[2, 1] * (all_hub_y[i] - all_wheel_y[i]) + R[
                2, 2] * (all_hub_z[i] - all_wheel_z[i])

            rotated_displacement_magnitudes = [np.sqrt(disp_x_rot[i] ** 2 + disp_y_rot[i] ** 2 + disp_z_rot[i] ** 2) for
                                               i in range(len(all_hub_y))]
            # plt.plot(rotated_displacement_magnitudes)
            holder = [(x - rotated_displacement_magnitudes[i - 1]) * .0393701 for i, x in enumerate(rotated_displacement_magnitudes)][1:]

            max_rotated_deformation_magnitude = max(holder)
            max_list.append(max_rotated_deformation_magnitude)

            plt.plot(holder)

        mean = np.nanmean(max_list, axis=0)
        # plt.plot(max_list)
        print(max_list)
        plt.show()
        #141

    return clean_list_df
