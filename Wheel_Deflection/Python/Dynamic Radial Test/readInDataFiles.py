import pandas as pd
import numpy as np
from os import listdir

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
    weight = []
    height = []
    for file in files:
        path = folder_dir + "/" + file.title()
        DF = pd.read_csv(path, header=2, low_memory=False)

        weight.append(str(path).split('_')[7].split('Klbf')[0][-4:])
        height.append(str(path).split('_')[5][len("Height"):])

        DF = DF.drop(index=0)
        DF = DF.drop(index=1)

        DF = fixMocapDF(DF)
        DF = DF.drop(index=2)

        DF.set_index('Frame', inplace=True)

        combinedCSVs.append(DF)
    return combinedCSVs, weight, height


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
Mocap data processing function

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
    clean_list_df = []
    # Find the MTS head column
    for df in list_df:
        # Getting all the y values of each marker and finding the max
        firstRow = df.iloc[0]
        YVals = firstRow[2::3].astype(float)

        maxY = max(YVals)

        # Labeling the columns corresponding to the rim top marker
        for index in YVals.index:
            if YVals[index] == maxY:
                # Rim Top Y Column -> rimTopY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'rim_top_y'}, inplace=True)
                df.rename(columns={df.columns[num_index - 1]: 'rim_top_x'}, inplace=True)
                df.rename(columns={df.columns[num_index + 1]: 'rim_top_z'}, inplace=True)
                YVals = YVals.drop(index)

        # recalculate max to find axel column
        maxY = max(YVals)

        for index in YVals.index:
            if YVals[index] == maxY:
                # Axel Top Y Column -> axelY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'axel_y'}, inplace=True)
                df.rename(columns={df.columns[num_index - 1]: 'axel_x'}, inplace=True)
                df.rename(columns={df.columns[num_index + 1]: 'axel_z'}, inplace=True)
                YVals = YVals.drop(index)

        # Re-labelling the xyz columns of the stand marker
        num_index = df.columns.get_loc(YVals.index[0])
        df.rename(columns={df.columns[num_index]: 'stand_y'}, inplace=True)
        df.rename(columns={df.columns[num_index - 1]: 'stand_x'}, inplace=True)
        df.rename(columns={df.columns[num_index + 1]: 'stand_z'}, inplace=True)

        # finds original distance between the stand and rim markers
        firstRow = df.iloc[0]

        distRimStand0 = {}

        distRimStandx = float(firstRow['rim_top_x']) - float(firstRow['stand_x'])
        distRimStand0["x"] = distRimStandx

        distRimStandy = float(firstRow['rim_top_y']) - float(firstRow['stand_y'])
        distRimStand0["y"] = distRimStandy

        distRimStandz = float(firstRow['rim_top_z']) - float(firstRow['stand_z'])
        distRimStand0["z"] = distRimStandz

        # Converting these columns to have type float
        df['rim_top_x'] = pd.to_numeric(df['rim_top_x'], errors='coerce')
        df['rim_top_y'] = pd.to_numeric(df['rim_top_y'], errors='coerce')
        df['rim_top_z'] = pd.to_numeric(df['rim_top_z'], errors='coerce')
        df['stand_x'] = pd.to_numeric(df['stand_x'], errors='coerce')
        df['stand_y'] = pd.to_numeric(df['stand_y'], errors='coerce')
        df['stand_z'] = pd.to_numeric(df['stand_z'], errors='coerce')
        df['Time (sec)'] = pd.to_numeric(df['Time (sec)'], errors='coerce')

        """"
        first finds the distance between the stand and rim for each point in time
        and subtracts the original distance to filter out noise from the stand
        moving due to the carrige and piston catch
        """

        dataLength = len(df)
        distRimStand = {}

        df['Displacementx'] = distRimStand0["x"] - (df['rim_top_x'] - df['stand_x'])
        df['Displacementy'] = distRimStand0["y"] - (df['rim_top_y'] - df['stand_y'])
        df['Displacementz'] = distRimStand0["z"] - (df['rim_top_z'] - df['stand_z'])

        # Get max/min displacement y as a var for fun ig
        maxDisY = max(df['Displacementy'])
        minDisY = min(df['Displacementy'])

        clean_list_df.append(df)

    return clean_list_df

