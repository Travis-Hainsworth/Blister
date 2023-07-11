from graphingFunctions import *
from settlingTime import find_settling_time

# x-axis is force. If you want the lateral plot then change do_you_want_lateral to 'yes'
# radial_plot_weight(r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Rock")

# x-axis is drop height. If you want the lateral plot then change do_you_want_lateral to 'yes'
# radial_plot_height(r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Rock")

deformations, weights, heights, rims, heads = processor([
        r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\Stans\Test_7-5_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\Stans\Test_7-5_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\Light\Test_7-5_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\Light\Test_7-5_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\R30\Test_7-6_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\R30\Test_7-6_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\DTS\Test_7-10_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\DTS\Test_7-10_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\Enve\Test_7-8_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\Enve\Test_7-8_Flat"
])

# comparison plot height on the x_axis
comparison_plot_mean(deformations, heights, rims, heads)

# comparison plot weight on the x_axis
comparison_plot_mean_weight(deformations, weights, rims, heads)

# comparison plot with force on the x-axis and drop height on the y-axis
comparison_plot_weight_height(deformations, weights, heights, rims, heads)

# comparison plot between carbon and alloy rims height on the x_axis
carbon_vs_alloy_plot(deformations, heights, rims, heads)
