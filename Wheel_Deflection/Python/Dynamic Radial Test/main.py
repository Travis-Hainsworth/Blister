import numpy as np
from dampingAnalysisMain import dataProcessingMain
import plotly.graph_objects as go

mocap, fftData, max_defs, weight = dataProcessingMain(r"C:\Users\ethan\Downloads\OneDrive_2023-06-29 (1)\Testing 6-29-23", plot=False)
mocap_flat, fftData_flat, max_defs_flat, weight_flat = dataProcessingMain(r"C:\Users\ethan\Downloads\OneDrive_2023-06-29 (1)\Testing 6-28-23", plot=False)

max_def_inches = [i * .0393701 for i in max_defs]
max_def_inches_flat = [i * .0393701 for i in max_defs_flat]


weight = np.array(weight).astype(float)
max_def_inches = np.negative(max_def_inches)

weight_flat = np.array(weight_flat).astype(float)
max_def_inches_flat = np.negative(max_def_inches_flat)

# Sort the data based on weight values
sorted_indices = np.argsort(weight)
sorted_weight = weight[sorted_indices]
sorted_max_def_inches = max_def_inches[sorted_indices]

sorted_indices_flat = np.argsort(weight_flat)
sorted_weight_flat = weight_flat[sorted_indices_flat]
sorted_max_def_inches_flat = max_def_inches_flat[sorted_indices_flat]

# Perform degree 2 polynomial regression
regression_coefficients = np.polyfit(sorted_weight, sorted_max_def_inches, 2)
regression_curve = np.polyval(regression_coefficients, sorted_weight)

regression_coefficients_flat = np.polyfit(sorted_weight_flat, sorted_max_def_inches_flat, 1)
regression_curve_flat = np.polyval(regression_coefficients_flat, sorted_weight_flat)
print(regression_coefficients_flat)

fig = go.Figure()
fig.add_trace(go.Scatter(x=sorted_weight, y=sorted_max_def_inches, mode='markers', marker=dict(size=8), name='Drop Height Fake Rock'))
fig.add_trace(go.Scatter(x=sorted_weight, y=regression_curve, mode='lines', name='Degree 2 Regression Curve Fake Rock'))

fig.add_trace(go.Scatter(x=sorted_weight_flat, y=sorted_max_def_inches_flat, mode='markers', marker=dict(size=8), name='Drop Height Flat Head'))
fig.add_trace(go.Scatter(x=sorted_weight_flat, y=regression_curve_flat, mode='lines', name='Degree 1 Regression Curve Flat Head'))
fig.add_trace(go.Scatter(x=sorted_weight, y=sorted_weight*-3.7e-05+.00123, mode='lines', name='Static Testing Regression'))

fig.update_layout(
    title='Max Deformation per Trial',
    xaxis=dict(title='Force (klbf)'),
    yaxis=dict(title='Compression (in)'),
    showlegend=True
)

fig.show()

# find_settling_time(fftData)
