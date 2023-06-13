import matplotlib.pyplot as plt
from dataProcessing import *
"""
PLots a shaded error bar graph of all tests performed. Shaded region is +/- 1 standard deviation.
Also plots the individual tests.
All the inputs come from the interpolate_data function.
"""


def plot_interpolated_data(displacements, mean_of_displacements, std_of_displacements, independent_variable):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(np.arange(0, 701, 100))

    # Shaded error graph
    plt.subplot(121)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    lower_bound = mean_of_displacements - std_of_displacements
    upper_bound = mean_of_displacements + std_of_displacements

    plt.suptitle('Quasi-Static Loading on Bike Rims with Tires')
    plt.title('Shaded Region: +/- 1 sigma')

    plt.fill_between(independent_variable, lower_bound, upper_bound, color='green', alpha=.15)
    plt.plot(independent_variable, mean_of_displacements, color='gray')

    plt.setp(plt.gca().lines, linewidth=1)

    # Individual test graph
    plt.subplot(122)
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    plt.title('Individual test data')
    for i in range(displacements.shape[0]):
        plt.plot(independent_variable, displacements[i])

    plt.show()

