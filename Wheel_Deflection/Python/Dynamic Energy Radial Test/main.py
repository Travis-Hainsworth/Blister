import matplotlib.pyplot as plt

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
    r"C:\Users\ethan\Test\Energy_Testing\R30_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\R30_Rock",
    r"C:\Users\ethan\Test\Energy_Testing\Light_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\Light_Rock",
    r"C:\Users\ethan\Test\Energy_Testing\R30AL_Flat",
    r"C:\Users\ethan\Test\Energy_Testing\R30AL_Rock",
    # r"C:\Users\ethan\Test\Energy_Testing\Flat_Test"

])
# pro.disable()
# pro.print_stats(sort='cumtime')
percent_diff_plot(energy_absorbed, drop_heights, rims, heads)
height_vs_displacement(drop_heights, displacement, rims, heads)
energy_vs_displacement(energy_absorbed, displacement, rims, heads, norm=True)
energy_vs_displacement(energy_absorbed, displacement, rims, heads, norm=False)


