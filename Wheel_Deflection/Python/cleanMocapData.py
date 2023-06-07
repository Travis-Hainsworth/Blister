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


def clean_mocap_data(file_path):
    mocap = pd.read_csv(file_path, skiprows=7)

    # Find the MTS head column
    i = max(mocap.iloc[1, :])
    max_height = max(mocap.iloc[:, 1])

    y_vars = np.array(mocap.iloc[:, 3::3])

    for i in range(3):
        if y_vars[1, i] == max_height:
            y_vars[2, i] = 0

    rim_top_index = np.argmax(y_vars[0, :])
    y_vars = np.delete(y_vars, rim_top_index, 1)
    rim_top = (rim_top_index-1)*3+4

    center_index = np.argmax(y_vars[0, :])
    center = (center_index-1)*3+4

    mo_head_height = mocap[:, i]
    mo_head_height = mo_head_height - mo_head_height[1]
    mo_head_height = -mo_head_height

    thresh = .05
    starting_index = np.argmax(mo_head_height > thresh)

    peak_height = max(mo_head_height)
    thresh = .025

    index_of_top_height = np.argmax(mo_head_height > peak_height-thresh)
    print("hello")
    #mocap = mocap(starting_index:index_of_top_height, :)


clean_mocap_data(r"C:\Users\ethan\Test\WAOU700lbf.csv")

