import numpy as np
from dampingAnalysisMain import dataProcessingMain
import plotly.graph_objects as go


def radial_and_lateral_plots(file_path):
    mocap, fftData, max_defs, weight, _ = dataProcessingMain(file_path, axis='y')
    mocap_lat, fftData_lat, max_defs_lat, weight_lat, _ = dataProcessingMain(file_path, axis='z')

    max_def_inches = [i * .0393701 for i in max_defs]
    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    weight = np.array(weight).astype(float)
    max_def_inches = np.negative(max_def_inches)

    weight_lat = np.array(weight_lat).astype(float)
    max_def_inches_lat = np.negative(max_def_inches_lat)

    # Sort the data based on weight values
    sorted_indices = np.argsort(weight)
    sorted_weight = weight[sorted_indices]
    sorted_max_def_inches = max_def_inches[sorted_indices]

    sorted_indices_lat = np.argsort(weight_lat)
    sorted_weight_lat = weight_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    # Perform degree 2 polynomial regression
    regression_coefficients = np.polyfit(sorted_weight, sorted_max_def_inches, 2)
    regression_curve = np.polyval(regression_coefficients, sorted_weight)

    regression_coefficients_lat = np.polyfit(sorted_weight_lat, sorted_max_def_inches_lat, 2)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_weight_lat)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_weight, y=sorted_max_def_inches, mode='markers', marker=dict(size=8), name='Test Fake Rock'))
    fig.add_trace(go.Scatter(x=sorted_weight, y=regression_curve, mode='lines', name='Degree 2 Regression Curve Radial'))

    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8), name='Test Fake Rock'))
    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=regression_curve_lat, mode='lines', name='Degree 2 Regression Curve Lateral'))

    fig.update_layout(
        title='Max Deformation per Trial',
        xaxis=dict(title='Force (klbf)'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True
    )

    fig.show()

