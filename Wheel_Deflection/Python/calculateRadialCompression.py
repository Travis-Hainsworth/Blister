import numpy as np
import pandas as pd
import random
from scipy.signal import convolve
from sklearn.neighbors import LocalOutlierFactor

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


def get_useful_markers(mocap_synced, axle_column, rim_top_column):
    rim_top_marker = mocap_synced.iloc[:, rim_top_column - 1:rim_top_column + 2]
    axle_marker = mocap_synced.iloc[:, axle_column - 1:axle_column + 2]

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
    radial_length = np.sqrt(np.sum(radial_vector ** 2, axis=1))

    # Calculate radial compression by removing the first value from every value so the data starts at (0, 0)
    radial_compression = [x - radial_length[0] for x in radial_length]
    [radial_compression.remove(x) for x in radial_compression if x < -.04 or x > .05]

    # Calculate the moving average to help reduce noise
    window_size = 50
    radial_compression_smooth = convolve(radial_compression, np.ones(window_size) / window_size, mode='valid')

    if smooth:
        return radial_compression
    else:
        return radial_compression_smooth


# def replace_outliers_with_mean(data, threshold=3):
#     median = np.median(data)
#     mad = np.median([np.abs(x - median) for x in data])
#     modified_z_scores = [0.6745 * (x - median) / mad for x in data]  # Scaling factor for asymptotic consistency
#
#     outliers = np.where(np.abs(modified_z_scores) > threshold)[0]
#
#     for index in outliers:
#         # Find the indices of nearby values within a certain range (e.g., within 2 indices)
#         nearby_indices = [i for i in range(len(data)) if abs(i - index) <= 1000]
#
#         # Calculate the mean of nearby values excluding the outlier
#         mean = np.mean([data[i] for i in nearby_indices])
#
#         # Replace the outlier with the calculated mean
#         data[index] = mean
#
#     return data

# def replace_outliers_with_mean(data, neighbors=500):
#     # Create an instance of LocalOutlierFactor
#     lof = LocalOutlierFactor(n_neighbors=neighbors)
#
#     # Convert the data list to a NumPy array and reshape it for input to LOF
#     data_array = np.array(data).reshape(-1, 1)
#
#     # Fit the data and obtain the anomaly scores
#     scores = lof.fit_predict(data_array)
#
#     # Replace outliers with the mean of nearby data points
#     for i, score in enumerate(scores):
#         if score == -1:
#             # Reshape the data point to have a single feature
#             data_point = np.array(data[i]).reshape(1, -1)
#
#             # Find the indices of the k nearest neighbors
#             indices = lof.kneighbors(data_point, n_neighbors=neighbors, return_distance=False)[0]
#
#             # Calculate the mean of nearby data points excluding the outlier itself
#             mean = np.mean([data[idx] for idx in indices if idx != i])
#
#             # Replace the outlier with the calculated mean
#             data[i] = mean
#
#     return data

def replace_outliers_with_random(data, neighbors=15, lower_bound=-0.04, upper_bound=0.005):
    # Create an instance of LocalOutlierFactor
    lof = LocalOutlierFactor(n_neighbors=neighbors)

    # Convert the data list to a NumPy array and reshape it for input to LOF
    data_array = np.array(data).reshape(-1, 1)

    # Fit the data and obtain the anomaly scores
    scores = lof.fit_predict(data_array)

    # Replace outliers with random values based on nearby data points
    for i, score in enumerate(scores):
        if score == -1:
            # Find the indices of the k nearest neighbors within the bounds
            indices = [idx for idx in lof.kneighbors([[data[i]]], n_neighbors=neighbors, return_distance=False)[0]
                       if lower_bound <= data[idx] <= upper_bound]

            # Generate a random value based on nearby data points within the bounds
            random_value = random.choice([data[idx] for idx in indices])

            # Replace the outlier with the random value
            data[i] = random_value

    return data





