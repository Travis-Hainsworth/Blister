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
import numpy as np
import pandas as pd


def clean_mocap_data(mocap):
    #mocap = pd.read_csv(file_path, skiprows=7)

    # Find the MTS head column
    firstRow = mocap.iloc[0]
    YVals = firstRow[3::3]
    maxY = max(YVals)
    
    end = len(mocap.columns)
    firstRow = mocap.iloc[0]
    YVals = firstRow[3::3]
    maxY = max(YVals)

    findingRimTop = YVals
    for val in findingRimTop.index:
        if(findingRimTop[val] == maxY):
            #MTS Head Column -> mtsHeadY
            mtsHeadY = val
            YVals = YVals.drop(val)

    secondMaxY = max(YVals)

    for val in YVals.index:
        if(YVals[val] == secondMaxY):
            #Rim Top Column -> rimTopY
            rimTopY = val
            YVals = YVals.drop(val)

    thirdMaxY = max(YVals)
    minY = min(YVals)

    for val in YVals.index:
        if(YVals[val] == thirdMaxY):
            #Center Hub Column -> centerY
            centerY = val
        elif(YVals[val] == minY):
            #Bottom Rim Column -> bottomRimY
            bottomRimY = val

    findingRimTop[mtsHeadY] = maxY

    MTSHeadYCol = testDF[mtsHeadY]

    start = False
    index = 3
    maxYFloat = float(maxY)
    
    
    #Finding row where MTS Head starts to move (allegedly) -> startIndex
    while(start == False):
        val = float(MTSHeadYCol[index])
        if(val < maxYFloat-0.05):
            start = True
            startIndex = index
        index = index+1
    
    #dropping all values in the dataframe before the start index
    mocap = mocap.drop(mocap.index[:startIndex])

    #Still need to find the "end" of the test. Previous group
    #was finding the row where the MTS head had reached back to the
    #original starting height.


clean_mocap_data(r"C:\Users\ethan\Test\WAOU700lbf.csv")

