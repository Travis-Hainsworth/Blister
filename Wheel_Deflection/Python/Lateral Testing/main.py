from dataProcessing import processor
from graphingFunctions import *

deformations, rims = processor([
    r"C:\Users\ethan\Test\Static_Lateral\R30",
    r"C:\Users\ethan\Test\Static_Lateral\Stans Flow"
])

lateral_plot(deformations, rims)
