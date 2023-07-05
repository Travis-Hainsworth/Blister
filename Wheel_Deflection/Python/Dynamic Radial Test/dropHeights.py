import numpy as np
from dampingAnalysisMain import dataProcessingMain
import plotly.graph_objects as go


def radial_and_lateral_drop_height_plot(file_path):
    mocap, fftData, max_defs, _, height = dataProcessingMain(file_path, axis='y')
    mocap_lat, fftData_lat, max_defs_lat, _, height_lat = dataProcessingMain(file_path, axis='z')

    max_def_inches = [i * .0393701 for i in max_defs]
    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    height = np.array(height).astype(int)
    max_def_inches = np.negative(max_def_inches)

    height_lat = np.array(height_lat).astype(int)
    max_def_inches_lat = np.negative(max_def_inches_lat)

    # Sort the data based on weight values
    sorted_indices = np.argsort(height)
    sorted_height = height[sorted_indices]
    sorted_max_def_inches = max_def_inches[sorted_indices]

    sorted_indices_lat = np.argsort(height_lat)
    sorted_height_lat = height_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    # Perform degree 2 polynomial regression
    regression_coefficients = np.polyfit(sorted_height, sorted_max_def_inches, 2)
    regression_curve = np.polyval(regression_coefficients, sorted_height_lat)

    regression_coefficients_lat = np.polyfit(sorted_height_lat, sorted_max_def_inches_lat, 2)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_height_lat)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_height, y=sorted_max_def_inches, mode='markers', marker=dict(size=8), name='Test Fake Rock'))
    fig.add_trace(go.Scatter(x=sorted_height, y=regression_curve, mode='lines', name='Degree 2 Regression Curve Radial'))

    fig.add_trace(go.Scatter(x=sorted_height_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8), name='Test Fake Rock'))
    fig.add_trace(go.Scatter(x=sorted_height_lat, y=regression_curve_lat, mode='lines', name='Degree 2 Regression Curve Lateral'))

    fig.update_layout(
        title='Max Deformation per Trial',
        xaxis=dict(title='Drop Height'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True
    )

    fig.show()

