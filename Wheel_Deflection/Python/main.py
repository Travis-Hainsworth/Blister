from graphFunctions import *

# If you want to see the non-smoothed data add "True" to the after the list folder path.
# For the file paths don't remove the "r" from the front of the path
# Mocap data then MTS data
# ex: r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New"
# If you want to see the un-smoothed data then add "True" after the last file path.

################################################### NEW DATA ###########################################################
# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\Stans_Mocap\Stans_Best",
#                              r"C:\Users\ethan\Test\Static_New_Data\Stans_MTS\Stans_Best")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\ENVE_Mocap\ENVE_Best",
#                              r"C:\Users\ethan\Test\Static_New_Data\ENVE_MTS\ENVE_Best")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\Lite_Mocap\Lite_Best",
#                              r"C:\Users\ethan\Test\Static_New_Data\Lite_MTS\Lite_Best")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\WAOU_Mocap\6-16",
#                              r"C:\Users\ethan\Test\Static_New_Data\WAOU_MTS\6-16")

final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\R30_Mocap\6-16",
                             r"C:\Users\ethan\Test\Static_New_Data\R30_MTS\6-16")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\R30_Mocap\6-16",
#                              r"C:\Users\ethan\Test\Static_New_Data\R30_MTS\6-16")

# final_data = data_processing(r"C:\Users\ethan\Test\Static_New_Data\R30_Mocap\6-16",
#                              r"C:\Users\ethan\Test\Static_New_Data\R30_MTS\6-16")

########################################################################################################################

################################################### OLD DATA ###########################################################
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
#
rims = ['Enve', 'Stans', 'Lite', 'R30', 'WAOU']
# rims = ['R30', 'Old R30']
good_data = [

    data_processing(r"C:\Users\ethan\Test\Static_New_Data\ENVE_Mocap\ENVE_Best",
                    r"C:\Users\ethan\Test\Static_New_Data\ENVE_MTS\ENVE_Best"),
    data_processing(r"C:\Users\ethan\Test\Static_New_Data\Stans_Mocap\Stans_Best",
                    r"C:\Users\ethan\Test\Static_New_Data\Stans_MTS\Stans_Best"),
    data_processing(r"C:\Users\ethan\Test\Static_New_Data\Lite_Mocap\6-16",
                    r"C:\Users\ethan\Test\Static_New_Data\Lite_MTS\6-16"),
    data_processing(r"C:\Users\ethan\Test\Static_New_Data\R30_Mocap\6-16",
                    r"C:\Users\ethan\Test\Static_New_Data\R30_MTS\6-16"),
    data_processing(r"C:\Users\ethan\Test\Static_New_Data\WAOU_Mocap\6-16",
                    r"C:\Users\ethan\Test\Static_New_Data\WAOU_MTS\6-16"),

    # data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\ENVE_Old_Data_Mocap",
    #                 r"C:\Users\ethan\Test\Old_MTS_Data\ENVE_Old_Data_MTS"),
    # data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\Lite_Old_Data_Mocap",
    #                 r"C:\Users\ethan\Test\Old_MTS_Data\Lite_Old_Data_MTS"),
    # data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\R30_Old_Data_Mocap",
    #                 r"C:\Users\ethan\Test\Old_MTS_Data\R30_Old_Data_MTS"),
    # data_processing(r"C:\Users\ethan\Test\Old_Mocap_Data\WAOU_Old_Data_Mocap",
    #                 r"C:\Users\ethan\Test\Old_MTS_Data\WAOU_Old_Data_MTS"),

]

mean_list = []
std_list = []
ind = []
for i in range(len(good_data)):
    mean, std, ind_var, _ = interpolate_data(good_data[i])
    mean_list.append(mean)
    std_list.append(std)
    ind.append(ind_var)

# mean, std, ind_var, disp = interpolate_data(final_data)
# plot_interpolated_data(disp, mean, std, ind_var)

multiple_rims_graph(mean_list, std_list, ind, rims)
