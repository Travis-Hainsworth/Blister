import threading
import pandas as pd
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
""""
Gets all MTS files within a folder. Make sure the files are named with a number
This function uses threading to read in multiple csvs at the same time to reduce the run time.

Input: 
folder_dir = path to the folder containing the MTS data

Output:
list_of_csvs = list of dataframes containing the data from all of the files with in the folder
"""


def get_mts_data(folder_dir):
    list_of_csvs = []
    files = os.listdir(folder_dir)
    files.sort()
    num_csv_files = sum(file.endswith('.csv') for file in files)
    list_of_csvs = num_csv_files * [None]
    lock = threading.RLock()

    def read_csv_file(index, file):
        if file.endswith('.csv'):
            try:
                path = os.path.join(folder_dir, file)
                df = pd.read_csv(path, header=6, low_memory=False, dtype=str)
                df = df.drop(index=0)
                df = df.rename(columns={'Crosshead ': 'Crosshead (in)', 'Load ': 'Load (lbf)', 'Time ': 'Time (sec)'})

                with lock:
                    list_of_csvs[index] = df
            except (pd.errors.EmptyDataError, pd.errors.ParserError):
                # Handle the error if the CSV file cannot be read or processed correctly
                print(f"Error processing file: {file}")

    with ThreadPoolExecutor() as executor:
        executor.map(read_csv_file, range(num_csv_files), files)

    return list_of_csvs


""""
Gets all mocap files within a folder. Make sure the files are named with a number.
This function uses threading to read in multiple csvs at the same time to reduce the run time.

Input: 
folder_dir = path to the folder containing the MTS data

Output:
combinedCSVs = list of dataframes containing the data from all of the files with in the folder
"""


def get_mocap_data(folder_dir):
    files = os.listdir(folder_dir)
    files.sort()
    num_csv_files = sum(file.endswith('.csv') for file in files)
    list_of_csvs = num_csv_files * [None]
    lock = threading.RLock()

    def read_csv_file(index, file):
        if file.endswith('.csv'):
            try:
                path = os.path.join(folder_dir, file)
                df = pd.read_csv(path, header=2, low_memory=False, dtype=str)
                df = df.drop([0, 1, 2])
                df = fix_mocap_df(df)

                with lock:
                    list_of_csvs[index] = df
            except (pd.errors.EmptyDataError, pd.errors.ParserError):
                # Handle the error if the CSV file cannot be read or processed correctly
                print(f"Error processing file: {file}")

    with ThreadPoolExecutor() as executor:
        executor.map(read_csv_file, range(num_csv_files), files)

    return list_of_csvs


"""
This function renames some of the important column names in the mocap data csv.
Used in the get_mocap_data function.

Input:
df = the dataframe with the mocap data

Output:
df: new dataframe with renamed columns
"""


def fix_mocap_df(df):
    first_row = np.array(df.iloc[0])
    new_cols = {'Unnamed: 0': 'Frame', 'Name': 'Time (sec)'}
    marker_name = ''
    for count, col in enumerate(df.columns[2:], start=2):
        marker_name = col if count % 3 == 0 else marker_name
        new_cols[col] = f"{marker_name} {first_row[count]}"

    df = df.rename(columns=new_cols)

    return df


""""
Makes the height and time columns start at (0, 0).
This function uses threading because it takes a really long time using one core.

Input:
list_df = list of dataframes from getMTSData

Output:
list_df = list of trimmed dataframes with updated "Crosshead (in)" and "Time (sec)" columns
"""


def clean_MTS_data(list_df):
    def clean_dataframe(df):
        crosshead_diff = np.double(df['Crosshead (in)'][1:]) - np.double(df['Crosshead (in)'][:-1])
        time_diff = np.double(df['Time (sec)'][1:]) - np.double(df['Time (sec)'][:-1])

        df['Crosshead (in)'] = np.concatenate(([0], crosshead_diff))
        df['Time (sec)'] = np.concatenate(([0], time_diff))

        return df

    with ThreadPoolExecutor() as executor:
        cleaned_data = list(executor.map(clean_dataframe, list_df))

    return cleaned_data


""""
This function clean the mocap data. It renames important columns and also trims some of the data that is found before
and after the compression since it is not important.

Input:
list_df = the list of all the motion capture data as dataframes.

Output:
clean_list_df = list of clean mocap data as dataframes.
"""


def clean_mocap_data(list_df):
    clean_list_df = []

    for df in list_df:
        firstRow = df.iloc[0]
        YVals = firstRow[3::3].astype(float)  # Convert to float type

        mts_head_y_index = YVals.idxmax()
        df.rename(columns={mts_head_y_index: 'mts_head_y'}, inplace=True)
        YVals = YVals.drop(mts_head_y_index)

        rim_top_y_index = YVals.idxmax()
        df.rename(columns={rim_top_y_index: 'rim_top_y'}, inplace=True)
        YVals = YVals.drop(rim_top_y_index)

        center_hub_y_index = YVals.idxmax()
        bottom_rim_y_index = YVals.idxmin()
        df.rename(columns={center_hub_y_index: 'center_hub_y', bottom_rim_y_index: 'bottom_rim_y'}, inplace=True)

        df['mts_head_y'] = np.double(df['mts_head_y']) - np.double(df.loc[3, 'mts_head_y'])
        df['mts_head_y'] = -df['mts_head_y']

        starting_index = df['mts_head_y'].gt(0.05).idxmax()

        peak_height = df['mts_head_y'].max()
        peak_height_index = df['mts_head_y'].gt(peak_height - 0.025).idxmax()
        df = df.iloc[starting_index:peak_height_index]

        clean_list_df.append(df)

    return clean_list_df


"""
If we want a force vs. displacement graph then we need the mocap data to
have the same sampling frequency as the MTS (plot(MTS load vs mocap height)).
Mocap has more data points so the amount of data points is getting equalized using a linear interpolation.

Input:
mocap_list = List of mocap dataframes.
mts_list = List of mts dataframes.

Output:
synced_df_list = List of interpolated mocap data as a dataframe.  
"""


def mocap_synced(mocap_list, mts_list):
    synced_df_list = []
    for counter in range(len(mocap_list)):
        ratio = mocap_list[counter].shape[0] / mts_list[counter].shape[0]
        indices = np.arange(0, mocap_list[counter].shape[0], ratio).astype(int)
        synced = mocap_list[counter].iloc[indices, :]

        # Reset the indexing of the data frames, so it starts at 0 instead of 3.
        synced_df_list.append(synced.reset_index(drop=True))

    return synced_df_list
