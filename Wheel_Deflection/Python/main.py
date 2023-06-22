from graphFunctions import *

# If you want to see the non-smoothed data add "True" to the after the list folder path.
# For the file paths don't remove the "r" from the front of the path
# Mocap data then MTS data
# ex: r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New"
# If you want to see the un-smoothed data then add "True" after the last file path.

# ################################################## SINGLE GRAPHS ###########################################################
# final_data = data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\ENVE_Mocap\6-21",
#                              r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\ENVE_MTS\6-21")

# final_data = data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Stans_Mocap\6-21",
#                              r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Stans_MTS\6-21")

# final_data = data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Light_Mocap\6-21",
#                              r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Light_MTS\6-21")

# final_data = data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\R30_Mocap\6-21",
#                              r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\R30_MTS\6-21")

# final_data = data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\WAOU_Mocap\6-21",
#                              r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\WAOU_MTS\6-21")
########################################################################################################################

rims = ['ENVE', 'Stans', 'Light', 'R30', 'WAOU']
good_data = [
    data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\ENVE_Mocap\6-21",
                    r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\ENVE_MTS\6-21"),

    data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Stans_Mocap\6-21",
                    r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Stans_MTS\6-21"),

    data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Light_Mocap\6-21",
                    r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\Light_MTS\6-21"),

    data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\R30_Mocap\6-21",
                    r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\R30_MTS\6-21"),

    data_processing(r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\WAOU_Mocap\6-21",
                    r"C:\Users\Rady-MoCapCamera\Desktop\Static_New_Data_Summer2023\WAOU_MTS\6-21"),

]

mean_list = []
std_list = []
ind = []

for i in range(len(good_data)):
    mean, std, ind_var, _ = interpolate_data(good_data[i])
    mean_list.append(mean)
    std_list.append(std)
    ind.append(ind_var)
multiple_rims_graph(mean_list, std_list, ind, rims)

# ######### SINGLE GRAPHING ##########
# mean, std, ind_var, disp = interpolate_data(final_data)
# plot_interpolated_data(disp, mean, std, ind_var)
