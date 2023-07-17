from graphingFunctions import *
import cProfile

# pro = cProfile.Profile()
# pro.enable()
energy_absorbed, displacement, drop_heights, rims, heads = file_processor([
    r"C:\Users\ethan\Test\Energy_Testing\Enve_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\Enve_Rock",
    r"C:\Users\ethan\Test\Energy_Testing\DTS_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\DTS_Rock",
    r"C:\Users\ethan\Test\Energy_Testing\Stans_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\Stans_Rock",
    r"C:\Users\ethan\Test\Energy_Testing\Waou_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\Waou_Rock",

])
# pro.disable()
# pro.print_stats(sort='cumtime')
percent_diff_plot(energy_absorbed, drop_heights, rims, heads)
height_vs_displacement(drop_heights, displacement, rims, heads)
energy_vs_displacement(energy_absorbed, displacement, rims, heads)

# plot_all_markers(drop_heights, dfs)