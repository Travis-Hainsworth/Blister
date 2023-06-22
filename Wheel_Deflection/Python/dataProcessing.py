from readInDataFiles import *
from calculateRadialCompression import *
from sklearn.linear_model import LinearRegression
"""
This function does everything from the "calculateRadialCompression.py" and "readInDataFiles.py" for you.

Input: 
mocap_folder_dir = The path to the folder containing the mocap data. 
mts_folder_dir = The path to the folder containing the MTS data.
noise = If you want to see the data without the moving mean calculation then add "True" to the end of the function 
call. The default is to always smooth the data.

Output:
synced_data = This is the end all list of dataframes from testing. It is cleaned, smoothed, and synced.
"""


def data_processing(mocap_folder_dir, mts_folder_dir, noise=False):
    # Import mocap data.
    list_mocap_data = get_mocap_data(mocap_folder_dir)
    clean_mocap = clean_mocap_data(list_mocap_data)

    # Import mts data.
    list_mts_data = get_mts_data(mts_folder_dir)
    clean_mts = clean_MTS_data(list_mts_data)

    # Make both of the files the same size.
    synced_data = mocap_synced(clean_mocap, clean_mts)

    pd.options.mode.chained_assignment = None  # Suppress the SettingWithCopyWarning

    for counter, df in enumerate(synced_data):
        column_names = df.columns

        rim_top_marker_data = df.iloc[:, column_names.get_loc('rim_top_y') - 1:column_names.get_loc('rim_top_y') + 2]
        axle_marker_data = df.iloc[:, column_names.get_loc('center_hub_y') - 1:column_names.get_loc('center_hub_y') + 2]

        radial_compression_data = calc_radial_compression(axle_marker_data, rim_top_marker_data, noise)
        # Convert the measurement into inches
        radial_compression_data_inches = [i * 0.0393701 for i in radial_compression_data]

        # Cut off the padding from the convolve in calc_radial_compression
        synced_data[counter] = synced_data[counter].iloc[0:len(radial_compression_data_inches)]

        # Add 2 new columns to the master dataframe
        synced_data[counter].loc[:, 'Compression (in)'] = np.double(radial_compression_data_inches)

        # Need to remove the padding that is added by the smoothing process, so it can be put into the dataframe.
        # Removing the pad from the front is generally better as loads from 0 to 0.5 are not important.
        pad = len(clean_mts[counter]) - len(synced_data[counter])
        synced_data[counter]['Load (lbf)'] = \
            np.double(clean_mts[counter]['Load (lbf)'][pad:])

    pd.options.mode.chained_assignment = 'warn'  # Restore the default setting

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
    # To make the error bars graph, you need 1 constant independent variable "Load (lbf)".
    min_loads = np.array([np.min(df['Load (lbf)']) for df in df_list])
    max_loads = np.array([np.max(df['Load (lbf)']) for df in df_list])

    independent_lower_bound = np.max(min_loads)
    independent_upper_bound = np.min(max_loads)

    # Set the scaling for the independent variable.
    independent_variable_scale = np.arange(independent_lower_bound, independent_upper_bound + 0.1, 0.1)

    # Interpolate each test's displacement onto the unified independent variable.
    displacements = np.zeros((len(independent_variable_scale), len(df_list)))

    for j, df in enumerate(df_list):
        actual_load = df['Load (lbf)']
        actual_displacement = df['Compression (in)']

        # Remove repeated loads and corresponding displacements.
        _, indices_of_not_repeated = np.unique(actual_load, return_index=True)
        actual_displacement = actual_displacement[indices_of_not_repeated]

        # Interpolate using a linear interpolation method.
        displacements[:, j] = np.interp(independent_variable_scale, actual_load[indices_of_not_repeated],
                                        actual_displacement)

    displacements = displacements.T
    independent_variable_scale = independent_variable_scale.T

    # nan values will be present if a repeated load is found, so you need to take the mean without the nan values.
    mean_displacements = np.nanmean(displacements, axis=0)
    std_displacements = np.nanstd(displacements, axis=0)

    return mean_displacements, std_displacements, independent_variable_scale, displacements


def spoke_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    return df


def find_line_equation(x, y):
    # Perform linear regression
    model = LinearRegression()
    model.fit(x, y)

    # Get the slope (m) and intercept (b)
    m = model.coef_[0]
    b = model.intercept_

    # Return the equation as a string
    return f"y = {m}x + {b}"

