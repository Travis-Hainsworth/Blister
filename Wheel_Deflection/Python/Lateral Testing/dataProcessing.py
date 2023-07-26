from readInDataFiles import *
import numpy as np


def data_processing_main(file_path, axis):
    list_mocap_data, weight, height, rim, head = get_mocap_data(file_path)
    list_mocap_data = clean_mocap_data(list_mocap_data)
    max_defs = []

    for i, df in enumerate(list_mocap_data):
        if axis == 'y':
            index_of_max_def = df['Displacementy'].argmax()
            max_def = df['Displacementy'][index_of_max_def]
            max_def = round(max_def, 4)

            max_defs.append(max_def)

        elif axis == 'z':
            index_of_max_def = df['Displacementz'].argmax()
            max_def = df['Displacementz'][index_of_max_def]
            max_def = round(max_def, 4)

            max_defs.append(max_def)

        else:
            index_of_max_def = df['Displacementx'].argmax()
            max_def = df['Displacementx'][index_of_max_def]
            max_def = round(max_def, 4)

            max_defs.append(max_def)

    return max_defs, rim


def processor(filepaths):
    deformations, rims = [], []
    for filepath in filepaths:
        max_defs, rim = data_processing_main(filepath, axis='y')
        deformations.append(max_defs)
        rims.append(rim)

    return deformations, rims