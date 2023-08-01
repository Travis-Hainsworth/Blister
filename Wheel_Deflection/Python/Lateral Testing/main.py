from graphFunctions import *
from dataProcessing import *

# Make sure the string you put into this list matches how it is in the file path.
# If it does not work change the file paths in dataProcessing.py
rims = ['R30 Alloy', 'R30 Carbon', 'Light', 'WAOU']
mocap_data, mts_data = process_lateral_data(rims)

plot_lateral_deformations(mocap_data, mts_data, rims)
