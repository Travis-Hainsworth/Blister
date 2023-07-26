from graphFunctions import *

# If you want to see the non-smoothed data add "True" to the after the list folder path.
# For the file paths don't remove the "r" from the front of the path
# Mocap data then MTS data
# ex: r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New"
# If you want to see the un-smoothed data then add "True" after the last file path.

# ################################################## SINGLE GRAPHS #####################################################
# final_data = data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\ENVE_Mocap\6-21",
#                              r"C:\Users\ethan\Test\6-21 cleaned data\ENVE_MTS\6-21")

final_data = data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\Stans_Mocap\6-21",
                             r"C:\Users\ethan\Test\6-21 cleaned data\Stans_MTS\6-21")

# final_data = data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\Light_Mocap\6-21",
#                              r"C:\Users\ethan\Test\6-21 cleaned data\Light_MTS\6-21")
#
# final_data = data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\R30_Mocap\6-21",
#                              r"C:\Users\ethan\Test\6-21 cleaned data\R30_MTS\6-21")

# final_data = data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\WAOU_Mocap\6-21",
#                              r"C:\Users\ethan\Test\6-21 cleaned data\WAOU_MTS\6-21")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\DTS_Mocap",
#                              r"C:\Users\ethan\Test\Static_New_Data\DTS_MTS")

#################################################### All Graphs ########################################################

# rims = ['ENVE', 'Stans', 'Light', 'R30', 'WAOU', 'DTS']
# good_data = [
#     data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\ENVE_Mocap\6-21",
#                     r"C:\Users\ethan\Test\6-21 cleaned data\ENVE_MTS\6-21"),
#
#     data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\Stans_Mocap\6-21",
#                     r"C:\Users\ethan\Test\6-21 cleaned data\Stans_MTS\6-21"),
#
#     data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\Light_Mocap\6-21",
#                     r"C:\Users\ethan\Test\6-21 cleaned data\Light_MTS\6-21"),
#
#     data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\R30_Mocap\6-21",
#                     r"C:\Users\ethan\Test\6-21 cleaned data\R30_MTS\6-21"),
#
#     data_processing(r"C:\Users\ethan\Test\6-21 cleaned data\WAOU_Mocap\6-21",
#                     r"C:\Users\ethan\Test\6-21 cleaned data\WAOU_MTS\6-21"),
#
#     data_processing(r"C:\Users\ethan\Test\Static_New_Data\DTS_Mocap",
#                              r"C:\Users\ethan\Test\Static_New_Data\DTS_MTS")
#
# ]
#
# mean_list = []
# std_list = []
# ind = []
#
# for i in range(len(good_data)):
#     mean, std, ind_var, _ = interpolate_data(good_data[i])
#     mean_list.append(mean)
#     std_list.append(std)
#     ind.append(ind_var)
# multiple_rims_graph(mean_list, std_list, ind, rims)

# ######### SINGLE GRAPHING ##########
mean, std, ind_var, disp = interpolate_data(final_data)
plot_interpolated_data(disp, mean, std, ind_var)
