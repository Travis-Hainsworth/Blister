import numpy as np
import pandas as pd
from scipy.signal import convolve
""""
Computes all of the radial compression metrics as well as smooth the data to reduce noise.

Input:
axle_marker_data = The y position values of the axle marker in a data frame.
rim_top_marker_data = The y position values of the top of the rim marker in a data frame.
noise = If you want to look at the noisy data, put 'True' in the function call.

Output:
radial_compression = The list of radial compression data including the noise.
or
radial_compression_smooth = Reduce noise of radial_compression using a moving average calculation.
"""


def calc_radial_compression(axle_marker_data, rim_top_marker_data, noise=False):
    # For some reason some data points in these dataframes are considered type 'str'.
    # These lines make every point numeric values.
    rim_top_marker_data = rim_top_marker_data.apply(pd.to_numeric, errors='coerce')
    axle_marker_data = axle_marker_data.apply(pd.to_numeric, errors='coerce')

    # Find the vector from the marker on the top of the rim and the center hub marker.
    radial_vector = rim_top_marker_data['rim_top_y'].sub(axle_marker_data['center_hub_y'])

    # Calculate Euclidian distance.
    radial_length = np.abs(radial_vector)

    # Remove the first value from every values so the compressions start at 0.
    radial_compression = radial_length.sub(radial_length.iloc[0])

    # Calculate moving mean to reduce noise. Uses a fft.
    window_size = 360  # If you set this to the refresh rate it will make the data very smooth.
    radial_compression_smooth = convolve(radial_compression, np.ones(window_size) / window_size, mode='valid')

    return radial_compression if noise else radial_compression_smooth


