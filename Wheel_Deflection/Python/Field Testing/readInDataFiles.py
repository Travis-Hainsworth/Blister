from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os
from dtypes import *
import multiprocessing

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

