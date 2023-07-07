from graphingFunctions import *

# x-axis is force. If you want the lateral plot then change do_you_want_lateral to 'yes'
# radial_and_lateral_plots(r"C:\Users\ethan\Test\Dynamic_Testing\Stans\Test_7-5_Flat",
#                          do_you_want_lateral='no')

# x-axis is drop height. If you want the lateral plot then change do_you_want_lateral to 'yes'
# radial_and_lateral_drop_height_plot(r"C:\Users\ethan\Test\Dynamic_Testing\Light\Testing Round 2",
#                                     do_you_want_lateral='no')

# comparison plot
comparison_plot_mean([
        r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\WAOU\Test_6-29_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\Stans\Test_7-5_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\Stans\Test_7-5_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\Light\Test_7-5_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\Light\Test_7-5_Flat",
        r"C:\Users\ethan\Test\Dynamic_Testing\R30\Test_7-6_Rock",
        r"C:\Users\ethan\Test\Dynamic_Testing\R30\Test_7-6_Flat"

])

