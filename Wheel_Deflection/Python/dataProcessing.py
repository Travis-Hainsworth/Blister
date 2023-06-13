from readInDataFiles import *
from calculateRadialCompression import *
"""
This function does everything from the "calculateRadialCompression.py" and "readInDataFiles.py" for you.

Input: 
filePathOptitrack = The path to the folder containing the mocap data. 
filePathMts = The path to the folder containing the MTS data.
smoothing = If you want to see the data without the moving mean calculation then add "True" to the end of the function 
call. The default is to always smooth the data.

Output:
synced_data = This is the end all list of dataframes from testing. It is cleaned, smoothed, and synced.
"""


def data_processing(filePathOptitrack, filePathMTS, smoothing=False):
    # Import mocap data. Make sure every file you want to look at is in the folder you input.
    list_mocap_data = getMocapData(filePathOptitrack)
    clean_mocap = clean_mocap_data(list_mocap_data)

    # Import mts data. Make sure every file you want to look at is in the folder you input.
    list_mts_data = getMTSData(filePathMTS)
    clean_mts = clean_MTS_data(list_mts_data)

    # Make both of the files the same size, so they can be graphed.
    synced_data = mocap_synced(clean_mocap, clean_mts)

    for counter in range(len(list_mocap_data)):
        column_names = synced_data[counter].columns
        axle_marker_data, rim_top_marker_data = get_useful_markers(synced_data[counter],
                                                                   column_names.get_loc('center_hub_y'),
                                                                   column_names.get_loc('rim_top_y'))

        radial_compression_data = calc_radial_compression(axle_marker_data, rim_top_marker_data, smoothing)
        # Convert the measurement into inches
        radial_compression_data_inches = [i * 0.0393701 for i in radial_compression_data]

        # Cut off the padding from the convolve in calc_radial_compression
        synced_data[counter] = synced_data[counter].iloc[0:len(radial_compression_data_inches)]

        # Add 2 new columns to the master dataframe
        synced_data[counter]['Compression (in)'] = np.double(radial_compression_data_inches)

        # Need to remove the padding that is added by the smoothing process, so it can be put into the dataframe.
        # Removing the pad from the front is generally better as loads from 0 to 0.5 are not important.
        pad = len(clean_mts[counter]) - len(synced_data[counter])
        synced_data[counter]['Load (lbf)'] = \
            np.double(clean_mts[counter]['Load (lbf)'][pad:])

    return synced_data


"""
To make the shaded error bars graph there needs to be a constant independent variable which in this case in the "Load".

Input: 
df_list = The list of dataframes from the testing. Should come from the "data_processing" function.

Output:
mean_displacements = The mean of interpolated displacements. Used for the shaded error bar.
std_displacements = The standard deviation of the interpolated displacements. Used for the shaded error bar.
independent_variable_scale = The unified x-axis or load values. Used for the shaded error bar graph.
displacements = The interpolated displacement values.
"""


def interpolate_data(df_list):
    # To make error bars, you need 1 constant independent variable "Load (lbf)"
    min_loads = np.zeros(len(df_list))
    max_loads = np.zeros(len(df_list))

    for i in range(len(df_list)):
        min_loads[i] = min(df_list[i]['Load (lbf)'])
        max_loads[i] = max(df_list[i]['Load (lbf)'])

    independent_lower_bound = max(min_loads)
    independent_upper_bound = min(max_loads)

    # This sets the scaling for the independent variable.
    independent_variable_scale = np.arange(independent_lower_bound, independent_upper_bound + .1, .1)

    # Interpolate each test's displacement onto the unified independent variable
    displacements = np.zeros((len(independent_variable_scale), len(df_list)))

    for j in range(len(df_list)):
        actual_load = df_list[j]['Load (lbf)']
        actual_displacement = df_list[j]['Compression (in)']
        
        # Remove repeated loads and the corresponding displacements
        actual_load, indices_of_not_repeated = np.unique(actual_load, return_index=True, return_inverse=False)
        actual_displacement = actual_displacement[indices_of_not_repeated]

        # Interpolate using a linear interpolation method
        displacements[:, j] = np.interp(independent_variable_scale, actual_load, actual_displacement)

    displacements = displacements.T
    independent_variable_scale = independent_variable_scale.T
    
    # nan values will be present if repeated load is found, so you need to take the mean without the nan values.
    mean_displacements = np.nanmean(displacements, axis=0)
    std_displacements = np.nanstd(displacements, axis=0)

    return mean_displacements, std_displacements, independent_variable_scale, displacements