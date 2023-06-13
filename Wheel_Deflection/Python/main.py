from graphFunctions import *

# If you want to see the non-smoothed data add "True" to the after the list folder path.
# For the file paths don't remove the "r" from the front of the path.
# Mocap data then MTS data
# ex: r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New"
# If you want to see the un-smoothed data then add "True" after the last file path.

################################################### NEW DATA ###########################################################
final_data = data_processing(r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New",
                             r"C:\Users\ethan\Test\ENVE_Static_MTS_Data_New")
########################################################################################################################

################################################### OLD DATA ############################################################
# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\ENVE_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\ENVE_Old_Data_MTS") # Very Bad

# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\DTS_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\DTS_Old_Data_MTS") # Good

# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\Lite_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\Lite_Old_Data_MTS") # Meh

# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\R30_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\R30_Old_Data_MTS") # Good

# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\STANS_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\STANS_Old_Data_MTS") # doesn't work

# final_data = data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\WAOU_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\Old_MTS_Data\WAOU_Old_Data_MTS") # Good
########################################################################################################################

mean, std, ind_var, disp = interpolate_data(final_data)
plot_interpolated_data(disp, mean, std, ind_var)
