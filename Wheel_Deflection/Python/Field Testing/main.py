from graphingFunctions import *
import multiprocessing as mp

import cProfile

# pro = cProfile.Profile()
# pro.enable()

energy_absorbed, displacement, rims = file_processor([
    r"C:\Users\ethan\Test\Field_Testing\Ref_Enve_Drop"
])

# energy_absorbed, displacement, rims = file_processor([
#     r"C:\Users\ethan\Test\Field_Testing\Skylar_Light"
# ])

# energy_absorbed, displacement, rims = file_processor([
#     r"C:\Users\ethan\Test\Field_Testing\Tyler_ENVE"
# ])
# pro.disable()
# pro.print_stats(sort='cumtime')
# percent_diff_plot(energy_absorbed, drop_heights, rims, heads)
# height_vs_displacement(drop_heights, displacement, rims, heads)
# energy_vs_displacement(energy_absorbed, displacement, rims, heads, norm=False)

