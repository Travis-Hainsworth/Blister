from matplotlib import pyplot as plt
from scipy import signal


def find_settling_time(fftData):
    for fft in fftData:
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.subplot(121)
        plt.plot(fft['Frequency (Hz)'], fft['|P1(f)|'])
        plt.xlabel('f (Hz)')
        plt.ylabel('|P1(f)|')
        plt.title('Not Welch')

        plt.subplot(122)
        plt.title('Welch')
        f, Pxx_den = signal.welch(fft['|P1(f)|'], fs=512, nperseg=256)
        plt.semilogy(f, Pxx_den)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('|P1(f)|')
        plt.show()

