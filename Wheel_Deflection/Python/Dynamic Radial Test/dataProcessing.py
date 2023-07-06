from math import ceil
from readInDataFiles import *
import pandas as pd
import numpy as np
from scipy.fft import fft


def dataProcessingMain(file_path, axis):
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

    return list_mocap_data, max_defs, weight, height, rim, head


def calc_r2(y_axis, regression_curve):
    residuals = y_axis - regression_curve

    tss = np.sum((y_axis - np.mean(y_axis)) ** 2)
    rss = np.sum(residuals ** 2)

    r2 = 1 - (rss / tss)

    return r2


def fft_analysis(df):
    # FFT analysis, finds natural frequency of rim

    # Find the index of the maximum y displacement (k)
    disp = df['Displacementy']
    k = disp.argmax()
    L = len(disp) - k + 1

    fft_arr = np.array(disp[k + 1:])
    Y = fft(fft_arr)

    p2 = abs(Y / L)
    p1_end = ceil(((L / 2) + 1))
    p1 = p2[0:p1_end]
    p1[2:(p1_end - 1)] = 2 * p1[2:(p1_end - 1)]

    f_arr = list(range(0, (ceil(L / 2) + 1)))
    f_arr = f_arr / L
    f_arr = f_arr * 500
    f_arr = f_arr[1:]
    p1 = p1[1:]

    fft_df = pd.DataFrame()
    fft_df['|P1(f)|'] = p1
    fft_df['Frequency (Hz)'] = f_arr

    return fft_df

