def find_settling_time(fftData, threshold):
    settling_times = []
    counter = 0

    for df in fftData:
        counter += 1
        # Find the frequency at which the amplitude drops below the threshold
        settling_freq = df.loc[df['|P1(f)|'] < threshold, 'Frequency (Hz)'].iloc[0]

        # Calculate the settling time as the inverse of the settling frequency
        settling_time = 1 / settling_freq
        settling_times.append((counter, settling_time/2))

    return settling_times
