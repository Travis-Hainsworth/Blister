import numpy as np
import pandas as pd
from scipy.signal import convolve
"""
Get the indices of the columns that pertain to the top of the rim marker and the axel marker.
Could be added upon to include other points of interest.

Input:
mocap_synced = Trimmed data from the motion capture.
axle_column = Index of the axle data in the dataframe.
rim_top_column = Index of the top of the rim data in the dataframe. 

Output:
axle_marker = All the data related to the axle marker.
rim_top_marker = All the data related to the rim_top marker.
"""


def get_useful_markers(mocap_synced,  axle_column, rim_top_column):

    rim_top_marker = mocap_synced.iloc[:, rim_top_column-1:rim_top_column+2]
    axle_marker = mocap_synced.iloc[:, axle_column-1:axle_column+2]

    return axle_marker, rim_top_marker


""""
Computes all of the radial compression metrics as well as smooth the data to reduce noise.

Input:
axle_marker_data = The y position values of the axle marker in a data frame.
rim_top_marker_data = The y position values of the top of the rim marker in a data frame.
smooth = If you want to look at the noisy data, put 'False' in the function call.

Output:
radial_compression = The list of radial compression data including the noise.
or
radial_compression_smooth = Reduce noise of radial_compression using a moving average calculation.
"""


def calc_radial_compression(axle_marker_data, rim_top_marker_data, smooth=True):

    # For some reason some data points in these data frames are considered type 'str'.
    # These 2 lines make all points into numeric values. It does not remove any data points.
    rim_top_marker_data = rim_top_marker_data.apply(pd.to_numeric, errors='coerce')
    axle_marker_data = axle_marker_data.apply(pd.to_numeric, errors='coerce')

    # Align the columns for subtraction to find radial vectors.
    rim_top_marker_data.columns = axle_marker_data.columns
    radial_vector = axle_marker_data - rim_top_marker_data

    # Calculate Euclidian length for each radial vector.
    radial_length = np.sqrt(np.sum(radial_vector**2, axis=1))

    # Calculate radial compression by removing the first value from every value so the data starts at (0, 0)
    radial_compression = [x - radial_length[0] for x in radial_length]
    # Calculate the moving average to help reduce noise
    window_size = 50
    radial_compression_smooth = convolve(radial_compression, np.ones(window_size) / window_size, mode='same')

    if smooth:
        return radial_compression
    else:
        return radial_compression_smooth

