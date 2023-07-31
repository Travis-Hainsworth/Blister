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
    firstRow = df.iloc[0]
    YVals = firstRow[3::3].astype(float)
    col = YVals.idxmin()
    df[col] = np.double(df[col]) - np.double(df[col].iloc[0])
    df = df.rename(columns={col: 'rim_y'})

    return df

