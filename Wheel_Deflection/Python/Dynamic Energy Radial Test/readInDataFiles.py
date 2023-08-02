from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
import os
import re
from dtypes import dtype_dict
import multiprocessing
import cProfile

NUM_CORES = multiprocessing.cpu_count()


def process_single_file(folder_dir, file):
    path = os.path.join(folder_dir, file.title())
    df = pd.read_csv(path, header=2, low_memory=False, dtype=dtype_dict)

    file_parts = str(path).split('_')
    height = file_parts[7].split("Height")[1]
    head = file_parts[9][:4]
    rim = file_parts[4]

    df = df.drop(index=[0, 1])
    df = fix_mocap_df(df)
    df = df.drop(index=2)
    df.set_index('Frame', inplace=True)

    return df, height, rim, head


# Function to process all CSV files in a folder using parallel processing
def get_mocap_data(folder_dir):
    files = sorted(os.listdir(folder_dir))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=NUM_CORES) as executor:
        processed_data = list(executor.map(process_single_file, [folder_dir] * len(files), files))

    # Unpack the results into separate lists
    combined_csvs, height, rim, head = zip(*processed_data)
    return combined_csvs, height, rim, head


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
    displacements = []
    pattern_drop_head = r'^Unlabeled \d+\.\d+ Y$'
    pattern_drop_head_special = r'^Unlabeled \d+ Y$'

    for df in list_df:
        drop_head = [col for col in df.columns if re.match(pattern_drop_head_special, col)]
        if len(drop_head) == 0:
            drop_head = [col for col in df.columns if re.match(pattern_drop_head, col)]
            drop_head_y = pd.to_numeric(df[drop_head[0]], errors='coerce')
        else:
            drop_head_y = pd.to_numeric(df[drop_head[0]], errors='coerce')

        important_info = pd.DataFrame()
        important_info['drop_head_y'] = drop_head_y

        if 'Wheel1:Marker 0deg.1 Y' in df.columns:
            rim_top_y = pd.to_numeric(df['Wheel1:Marker 0deg.1 Y'], errors='coerce')
            rim_hub_y = pd.to_numeric(df['Wheel1:Marker Hub.1 Y'], errors='coerce')

        elif 'RigidBody.1 Y' in df.columns:
            rim_top_y = pd.to_numeric(df['RigidBody:0deg.3 Y'], errors='coerce')
            rim_hub_y = pd.to_numeric(df['RigidBody:Hub.3 Y'], errors='coerce')

        else:
            rim_top_y = pd.to_numeric(df['RigidBody:Marker 0deg.1 Y'], errors='coerce')
            rim_hub_y = pd.to_numeric(df['RigidBody:Marker Hub.1 Y'], errors='coerce')

        displacement = np.abs(rim_hub_y - rim_top_y)
        max_displacement = displacement.min()
        scaled_displacement = max_displacement - displacement[0]

        displacements.append(scaled_displacement)
        clean_list_df.append(important_info)
    return clean_list_df, displacements

