from readInDataFiles import *
from calculateRadialCompression import *
import matplotlib.pyplot as plt

def dataProcessingMain(filePathOptitrack, filePathMTS):

    # Import mocap data. Make sure every file you want to look at is in the folder you input.
    # Don't remove the "r" before the file path.
    list_mocap_data = getMocapData(filePathOptitrack)
    clean_mocap = clean_mocap_data(list_mocap_data)

    # Import mts data. Make sure every file you want to look at is in the folder you input.
    # Don't remove the "r" before teh file path.
    list_mts_data = getMTSData(filePathMTS)#"r{}".format(filePath))
    clean_mts = clean_MTS_data(list_mts_data)

    # Make both of the files the same size so they can be graphed.
    synced_data = mocap_synced(clean_mocap, clean_mts)

    for counter in range(len(list_mocap_data)):
        column_names = synced_data[counter].columns
        axle_marker_data, rim_top_marker_data = get_useful_markers(synced_data[counter],
                                                                   column_names.get_loc('center_hub_y'),
                                                                   column_names.get_loc('rim_top_y'))
        radial_compression_data = calc_radial_compression(axle_marker_data, rim_top_marker_data)
        radial_compression_data_inches = [i * 0.0393701 for i in radial_compression_data]

        load_compression_data = pd.DataFrame({'Load (lbf)': np.double(clean_mts[counter]['Load (lbf)']),
                                              'Compression (in)': np.double(radial_compression_data_inches)})
        
        synced_data[counter]['Compression (in)'] = np.double(radial_compression_data_inches)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(load_compression_data['Load (lbf)'], load_compression_data['Compression (in)'])
        plt.ylabel('Compression (in)')
        plt.xlabel('Load (lbf)')
        ax.set_xticks(np.arange(0, 701, 100))
        plt.show()
        
    return synced_data

dataProcessingMain('/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/0_Data/DTS 2-10-23 Tire On/Optitrack Data', '/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/0_Data/DTS 2-10-23 Tire On/MTS Data')
