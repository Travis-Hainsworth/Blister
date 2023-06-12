from graphFunctions import *

# If you want to see the non-smoothed data add "True" to the after the list folder path.
# For the file paths don't remove the "r" from the front of the path.
# Mocap data then MTS data
# ex: r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New"
final_data = data_processing(r"C:\Users\ethan\Test\ENVE_Static_Mocap_Data_New",
                             r"C:\Users\ethan\Test\ENVE_Static_MTS_Data_New", False)

# final_data = data_processing(r"C:\Users\ethan\Test\ENVE_Old_Data_Mocap",
#                              r"C:\Users\ethan\Test\ENVE_Old_Data_MTS", False)

mean, std, ind_var, disp = interpolate_data(final_data)
plot_interpolated_data(disp, mean, std, ind_var)
