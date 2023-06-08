import math
import pandas as pd
import numpy as np
from os import listdir
""""
Gets all MTS files within a folder. Make sure the files are named with a number

Input: 
folder_dir = path to the folder containing the MTS data

Output:
combinedCSVs = list of dataframes containing the data from all of the files with in the folder
"""


def getMTSData(folder_dir):
    combinedCSVs = []
    files = listdir(folder_dir)
    files.sort()

    for file in files:
        path = folder_dir + "/" + file.title()
        DF = pd.read_csv(path, header=6)

        DF = DF.drop(index=0)

        DF = DF.rename(columns={'Crosshead ': 'Crosshead (in)', 'Load ': 'Load (lbf)', 'Time ': 'Time (sec)'})

        combinedCSVs.append(DF)

    return combinedCSVs


""""
Gets all mocap files within a folder. Make sure the files are named with a number

Input: 
folder_dir = path to the folder containing the MTS data

Output:
combinedCSVs = list of dataframes containing the data from all of the files with in the folder
"""


def getMocapData(folder_dir):
    combinedCSVs = []
    files = listdir(folder_dir)
    files.sort()

    for file in files:
        path = folder_dir + "/" + file.title()
        DF = pd.read_csv(path, header=2)

        DF = DF.drop(index=0)
        DF = DF.drop(index=1)

        DF = fixMocapDF(DF)

        DF = DF.drop(index=2)

        combinedCSVs.append(DF)

    return combinedCSVs


def fixMocapDF(DF):
    count = 0
    markerName = ''
    threeCount = 0
    newCols = {}
    firstRow = np.array(DF.iloc[0])
    for col in DF.columns:
        if count < 2:
            if count == 0:
                newCols['Unnamed: 0'] = 'Frame'
            else:
                newCols['Name'] = 'Time (sec)'
        else:
            if threeCount == 0:
                markerName = col
                newCols[col] = col + " " + firstRow[count]
                threeCount = threeCount + 1
            else:
                if threeCount == 2:
                    threeCount = -1
                newCols[col] = markerName + " " + firstRow[count]
                threeCount = threeCount + 1
        count = count + 1
    DF = DF.rename(columns=newCols, errors="raise")
    return DF


""""
Makes the height and time columns start at (0, 0)

Input:
list_df = list of data frames from getMTSData

Output:
list_df = list of trimmed dataframes with updated "Crosshead (in)" and "Time (sec)" columns
"""


def clean_MTS_data(list_df):
    for df in list_df:
        # Set the columns "Crosshead (in)" and "Time (sec)" to start at (0, 0)
        # by subtracting the first row from every row
        df['Crosshead (in)'] = [np.double(x) - np.double(df['Crosshead (in)'][1]) for x in df['Crosshead (in)']]
        df['Time (sec)'] = [np.double(y) - np.double(df['Time (sec)'][1]) for y in df['Time (sec)']]

    return list_df


""""
Mocap data processsing function

Input:
file_path = the path to the .csv file containing the data collected by the mocap system

Output:
mocap = matrix of the edited mocap data (trimmed to when the MTS test begins,
scaled values to match the MTS data, and reoriented values to match MTS)
rim_top = the matrix columns in mocap that represent the reflective dot  at the top of the rim
center = the matrix columns corresponding to the reflective dot in the center of the rim
i = index of the matrix column corresponding to the MTS head reflective dot
"""


def clean_mocap_data(list_df):
    # Find the MTS head column
    for df in list_df:
        firstRow = df.iloc[0]
        YVals = firstRow[3::3]

        firstRow = df.iloc[0]
        YVals = firstRow[3::3]
        maxY = max(YVals)

        findingRimTop = YVals

        for index in findingRimTop.index:
            if findingRimTop[index] == maxY:
                # MTS Head Column -> mtsHeadY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'mts_head_y'}, inplace=True)
                YVals = YVals.drop(index)

        secondMaxY = max(YVals)

        for index in YVals.index:
            if YVals[index] == secondMaxY:
                # Rim Top Column -> rimTopY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'rim_top_y'}, inplace=True)
                YVals = YVals.drop(index)

        thirdMaxY = max(YVals)
        minY = min(YVals)

        for index in YVals.index:
            if YVals[index] == thirdMaxY:
                # Center Hub Column -> centerY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'center_hub_y'}, inplace=True)
            elif YVals[index] == minY:
                # Bottom Rim Column -> bottomRimY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'bottom_rim_y'}, inplace=True)

        # Starts the mts height at zero then invert to match MTS orientation
        df['mts_head_y'] = [np.double(z) - np.double(df['mts_head_y'][3]) for z in df['mts_head_y']]
        df['mts_head_y'] = -df['mts_head_y']

        # Finding row where MTS Head starts to move (allegedly) -> startIndex
        starting_index = np.argmax(df['mts_head_y'] > .05)
        # Dropping all values in the dataframe before the start index
        df.drop(df.index[:starting_index])

        # Finding where the compression of the MTS ends
        peak_height = df['mts_head_y'].max()
        peak_height_index = np.argmax(df['mts_head_y'] > peak_height - .025)

        # Trimming all the mocap data based on the bounds
        df = df[starting_index:peak_height_index]

    return list_df


"""
If we want a force vs. displacement graph then we need the mocap data to
have the same sampling frequency as the MTS (plot(MTS load vs mocap height))

Mocap has more data points

Input:
mocap = individual mocap data
MTS = individual MTS data

Output:
synced = trimmed mocap data based upon size of MTS data
"""


def mocap_synced(mocap_list, mts_list):
    synced_df_list = []
    for counter in range(len(mocap_list)):
        ratio = mocap_list[counter].shape[0] / mts_list[counter].shape[0]
        synced = mocap_list[counter][0::math.ceil(ratio)]

        # Reset the indexing of the data frames so it starts at 0 instead of 3.
        synced_df_list.append(synced.reset_index(drop=True))

    return synced_df_list

