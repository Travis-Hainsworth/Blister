import pandas as pd
import numpy as np
import os
from os import listdir


def getMTSData(folder_dir):
    
    combinedCSVs = []
    
    for file in listdir(folder_dir):
        #Do these need to be labeled with their correct numbers?
        path = folder_dir + "/" + file.title()
        DF = pd.read_csv(path, header = 6)
        
        DF = DF.drop(index=0)
        
        DF = DF.rename(columns={'Crosshead ': 'Crosshead (in)', 'Load ': 'Load (lbf)', 'Time ': 'Time (sec)'})
        
        combinedCSVs.append(DF)
    
    return combinedCSVs

def getMocapData(folder_dir):
    
    combinedCSVs = []
    
    for file in listdir(folder_dir):
        
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
                         
                        