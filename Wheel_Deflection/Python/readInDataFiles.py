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
        DF = pd.read_csv(path, header = 2)
        
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
        if(count < 2):
            if(count == 0):
                newCols['Unnamed: 0'] = 'Frame'
            else:
                newCols['Name'] = 'Time (sec)'
        else:
            if(threeCount == 0):
                markerName = col
                newCols[col] = col + " " + firstRow[count]
                threeCount = threeCount+1
            else:
                if(threeCount == 2):
                    threeCount = -1
                newCols[col] = markerName +  " " + firstRow[count]
                threeCount = threeCount+1
        count = count+1
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

