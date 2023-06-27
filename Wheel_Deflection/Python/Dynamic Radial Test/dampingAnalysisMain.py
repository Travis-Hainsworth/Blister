from readInDataFiles import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dataProcessingMain(filePathOptitrack):

    # Import mocap data. Make sure every file you want to look at is in the folder you input.
    # Don't remove the "r" before the file path.
    list_mocap_data = getMocapData(filePathOptitrack)
    list_mocap_data = clean_mocap_data(list_mocap_data)

    for df in list_mocap_data:
        # Plot Y displacement over time
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Time (sec)'], df['Displacementy'])
        plt.ylabel('Displacement (mm)')
        plt.xlabel('Time (sec)')
        ax.set_xticks(np.linspace(0, 10, 10))
        plt.show()

dataProcessingMain(r"/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/0_Data/Dynamic Radial/Stans Flow 6-26-23 Tire On/Optitrack Data")