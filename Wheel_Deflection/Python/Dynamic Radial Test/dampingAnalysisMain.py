from math import ceil
from readInDataFiles import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft


def dataProcessingMain(file_path, plot=False):
    # Import mocap data. Make sure every file you want to look at is in the folder you input.
    # Don't remove the "r" before the file path.

    list_mocap_data, weight = getMocapData(file_path)
    list_mocap_data = clean_mocap_data(list_mocap_data)
    listFFTRes = []
    max_defs = []
    # fig, axs = plt.subplots(len(list_mocap_data), 2, figsize=(16, 8 * len(list_mocap_data)))

    for i, df in enumerate(list_mocap_data):
        # Plot Y displacement over time
        # axs[i, 0].plot(df['Time (sec)'], df['Displacementy'])
        indexOfMaxDef = df['Displacementy'].argmax()
        timeStamp = df['Time (sec)'][indexOfMaxDef]
        maxDef = df['Displacementy'][indexOfMaxDef]
        maxDef = round(maxDef, 4)
        dispString = "Max Deflection = " + str(maxDef)
        # axs[i, 0].text(timeStamp, maxDef, dispString)
        # axs[i, 0].scatter(timeStamp, maxDef, color='red', label=str(maxDef))
        # axs[i, 0].set_ylabel('Displacement (mm)')
        # axs[i, 0].set_xlabel('Time (sec)')
        # axs[i, 0].set_title('Dynamic Drop Displacement Over Time')
        # axs[i, 0].set_xticks(np.linspace(0, max(df['Time (sec)']), 10))
        # axs[i, 0].legend()

        FFTRes = fftAnalysis(df)
        listFFTRes.append(FFTRes)
        max_defs.append(maxDef)

        # Plot FFT analysis
        # axs[i, 1].plot(FFTRes['Frequency (Hz)'], FFTRes['|P1(f)|'])
        # axs[i, 1].set_title('Single-Sided Amplitude Spectrum of Displacement(t)')
        # axs[i, 1].set_xlabel('f (Hz)')
        # axs[i, 1].set_ylabel('|P1(f)|')

    # plt.tight_layout()
    # plt.subplots_adjust(wspace=.3, hspace=.5)
    # if plot:
    #     plt.show()
    # plt.clf()

    return list_mocap_data, listFFTRes, max_defs, weight


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