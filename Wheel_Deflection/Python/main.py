import numpy as np
from matplotlib import ticker

from readInDataFiles import *
from calculateRadialCompression import *
import matplotlib.pyplot as plt

list_mocap_data = getMocapData(r"C:\Users\ethan\Test\WAOU_Mocap_Data")
clean_mocap = clean_mocap_data(list_mocap_data)
list_mts_data = getMTSData(r"C:\Users\ethan\Test\WAOU_MTS_Data")
clean_mts = clean_MTS_data(list_mts_data)
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

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(load_compression_data['Load (lbf)'], load_compression_data['Compression (in)'])
    plt.ylabel('Compression (in)')
    plt.xlabel('Load (lbf)')
    ax.set_xticks(np.arange(0, 701, 100))
    plt.show()
