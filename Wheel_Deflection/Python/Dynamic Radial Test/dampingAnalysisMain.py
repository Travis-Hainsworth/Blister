from math import ceil

from readInDataFiles import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

def dataProcessingMain(filePathOptitrack):

    # Import mocap data. Make sure every file you want to look at is in the folder you input.
    # Don't remove the "r" before the file path.
    list_mocap_data = getMocapData(filePathOptitrack)
    list_mocap_data = clean_mocap_data(list_mocap_data)

    listFFTRes = []

    for df in list_mocap_data:
        # Plot Y displacement over time
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Time (sec)'], df['Displacementy'])
        indexOfMaxDef = df['Displacementy'].argmax()
        timeStamp = df['Time (sec)'][indexOfMaxDef]
        maxDef = df['Displacementy'][indexOfMaxDef]
        maxDef = round(maxDef, 4)
        dispString = "Max Deflection = " + str(maxDef)
        plt.text(timeStamp, maxDef, dispString)
        plt.ylabel('Displacement (mm)')
        plt.xlabel('Time (sec)')
        plt.title('Dynamic Drop Displacement Over Time')
        ax.set_xticks(np.linspace(0, max(df['Time (sec)']), 10))
        plt.show()
        FFTRes = fftAnalysis(df)
        listFFTRes.append(FFTRes)
    return (list_mocap_data, listFFTRes)

def fftAnalysis(df):
    # FFT analysis, finds natural frequency of rim

    # Find the index of the maximum y displacement (k)
    disp = df['Displacementy']
    k = disp.argmax()
    lenData = len(disp)
    L = lenData - k + 1

    # fft(realDisp(k+1:end,2))
    fftArr = np.array(disp[k + 1:])
    Y = fft(fftArr)

    # P1 = P2(1:L/2+1);
    P2 = abs(Y / L)
    P1end = ceil(((L / 2) + 1))
    P1 = P2[0:P1end]
    P1[2:(P1end - 1)] = 2 * P1[2:(P1end - 1)]

    # f = Fs*(0:(L/2))/L;
    fArr = list(range(0, (ceil(L / 2)+1)))
    fArr = fArr / L
    fArr = fArr * 500
    fArr = fArr[1:]
    P1 = P1[1:]
    print(len(P1))
    print(len(fArr))
    fftDF = pd.DataFrame()
    fftDF['|P1(f)|'] = P1
    fftDF['Frequency (Hz)'] = fArr

    plt.clf()
    plt.plot(fArr, P1)
    plt.title('Single-Sided Amplitude Spectrum of Displacement(t)')
    plt.xlabel('f (Hz)')
    plt.ylabel('|P1(f)|')
    plt.show()
    return fftDF

(mocap, fftData) = dataProcessingMain(r"/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/0_Data/Dynamic Radial/Stans Flow 6-26-23 Tire On/Optitrack Data")