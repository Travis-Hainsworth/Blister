from math import ceil
from readInDataFiles import *
import pandas as pd
import numpy as np
from scipy.fft import fft


def dataProcessingMain(file_path, axis):

    list_mocap_data, weight, height = getMocapData(file_path)
    list_mocap_data = clean_mocap_data(list_mocap_data)
    listFFTRes = []
    max_defs = []

    for i, df in enumerate(list_mocap_data):
        if axis == 'y':
            indexOfMaxDef = df['Displacementy'].argmax()
            maxDef = df['Displacementy'][indexOfMaxDef]
            maxDef = round(maxDef, 4)

            max_defs.append(maxDef)

        elif axis == 'z':
            indexOfMaxDef = df['Displacementz'].argmax()
            maxDef = df['Displacementz'][indexOfMaxDef]
            maxDef = round(maxDef, 4)

            max_defs.append(maxDef)

        else:
            indexOfMaxDef = df['Displacementx'].argmax()
            maxDef = df['Displacementx'][indexOfMaxDef]
            maxDef = round(maxDef, 4)

            max_defs.append(maxDef)

    return list_mocap_data, listFFTRes, max_defs, weight, height


def fftAnalysis(df):
    # FFT analysis, finds natural frequency of rim

    # Find the index of the maximum y displacement (k)
    disp = df['Displacementy']
    k = disp.argmax()
    lenData = len(disp)
    L = lenData - k + 1

    fftArr = np.array(disp[k + 1:])
    Y = fft(fftArr)

    P2 = abs(Y / L)
    P1end = ceil(((L / 2) + 1))
    P1 = P2[0:P1end]
    P1[2:(P1end - 1)] = 2 * P1[2:(P1end - 1)]

    fArr = list(range(0, (ceil(L / 2) + 1)))
    fArr = fArr / L
    fArr = fArr * 500
    fArr = fArr[1:]
    P1 = P1[1:]

    fftDF = pd.DataFrame()
    fftDF['|P1(f)|'] = P1
    fftDF['Frequency (Hz)'] = fArr

    return fftDF


def onclick(event):
    x, y = event.xdata, event.ydata
    print(f"Clicked at ({x}, {y})")