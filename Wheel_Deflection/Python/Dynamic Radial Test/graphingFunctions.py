import numpy as np
from dataProcessing import dataProcessingMain, calc_r2
import plotly.graph_objects as go


def radial_and_lateral_plots(file_path, do_you_want_lateral):
    mocap, max_defs, weight, _, rim, head = dataProcessingMain(file_path, axis='y')

    max_def_inches = [i * .0393701 for i in max_defs]

    weight = np.array(weight).astype(float)
    max_def_inches = np.negative(max_def_inches)

    # Sort the data based on weight values
    sorted_indices = np.argsort(weight)
    sorted_weight = weight[sorted_indices]
    sorted_max_def_inches = max_def_inches[sorted_indices]

    # Perform degree 2 polynomial regression
    regression_coefficients = np.polyfit(sorted_weight, sorted_max_def_inches, 2)
    regression_curve = np.polyval(regression_coefficients, sorted_weight)

    r2 = calc_r2(sorted_max_def_inches, regression_curve)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_weight, y=sorted_max_def_inches, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_weight, y=regression_curve, mode='lines',
                             name=f'Degree 2 Regression Curve Radial<br>r2 = {r2: .4f}'))

    if do_you_want_lateral == 'yes':
        lateral_plot_weight(file_path, fig)

    fig.update_layout(
        title=f'Max Deformation per Trial {rim} {head} head',
        xaxis=dict(title='Force (lbf)'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15)
    )

    fig.show()


def radial_and_lateral_drop_height_plot(file_path, do_you_want_lateral):
    mocap, max_defs, _, height, rim, head = dataProcessingMain(file_path, axis='y')

    max_def_inches = [i * .0393701 for i in max_defs]

    height = np.array(height).astype(int)
    max_def_inches = np.negative(max_def_inches)

    # Sort the data based on weight values
    sorted_indices = np.argsort(height)
    sorted_height = height[sorted_indices]
    sorted_max_def_inches = max_def_inches[sorted_indices]

    # Perform degree 2 polynomial regression
    regression_coefficients = np.polyfit(sorted_height, sorted_max_def_inches, 2)
    regression_curve = np.polyval(regression_coefficients, sorted_height)

    r2 = calc_r2(sorted_max_def_inches, regression_curve)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_height, y=sorted_max_def_inches, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_height, y=regression_curve, mode='lines',
                             name=f'Degree 2 Regression Curve Radial<br>r2 = {r2: .4f}'))

    if do_you_want_lateral == 'yes':
        lateral_plot_height(file_path, fig)

    fig.update_layout(
        title=f'Max Deformation per Trial {rim} {head} head',
        xaxis=dict(title='Drop Height'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15)
    )

    fig.show()


def comparison_plot_mean(file_paths):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Black', 'Orange', 'Pink', 'Bright Pink']

    for file_path in file_paths:
        mocap, max_defs, _, height, rim, head = dataProcessingMain(file_path, axis='y')

        max_def_inches = [i * .0393701 for i in max_defs]

        height = np.array(height).astype(float)
        max_def_inches = np.negative(max_def_inches)

        # Sort the data based on height values
        sorted_indices = np.argsort(height)
        sorted_height = height[sorted_indices]
        sorted_max_def_inches = max_def_inches[sorted_indices]

        mean_values = [np.mean(sorted_max_def_inches[sorted_height == value]) for value in np.unique(sorted_height)]

        regression_coefficients = np.polyfit(np.unique(sorted_height), mean_values, 3)
        regression_curve = np.polyval(regression_coefficients, np.unique(sorted_height))

        r2 = calc_r2(mean_values, regression_curve)

        if head == 'Flat':
            fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=regression_curve,
                                     mode='lines', marker=dict(symbol='x'),
                                     line=dict(dash='dash', color=colors[counter - 1]),
                                     name=f'Regression Curve Lateral {rim} {head}<br>r2 = {r2: .4f}'))
        elif head == 'Rock':
            fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=regression_curve,
                                     mode='lines', line=dict(color=colors[counter]),
                                     name=f'Regression Curve Lateral {rim} {head}<br>r2 = {r2: .4f}'))

        fig.update_layout(
            title='Max Deformation per Trial',
            xaxis=dict(title='Drop Height'),
            yaxis=dict(title='Compression (in)'),
            showlegend=True,
            font=dict(size=15),
        )
        counter += 1
    fig.show()


def lateral_plot_weight(file_path, fig):
    mocap_lat, max_defs_lat, weight_lat, height_lat, _, head = dataProcessingMain(file_path, axis='z')

    weight_lat = np.array(weight_lat).astype(float)
    height_lat = np.array(height_lat).astype(int)
    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    max_def_inches_lat = np.negative(max_def_inches_lat)
    sorted_indices_lat = np.argsort(weight_lat)

    sorted_weight_lat = weight_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    regression_coefficients_lat = np.polyfit(sorted_weight_lat, sorted_max_def_inches_lat, 2)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_weight_lat)

    r2_lat = calc_r2(sorted_max_def_inches_lat, regression_curve_lat)

    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=regression_curve_lat, mode='lines',
                             name=f'Degree 2 Regression Curve Lateral {head}<br>r2 = {r2_lat: .4f}'))


def lateral_plot_height(file_path, fig):
    mocap_lat, max_defs_lat, _, height_lat, _, head = dataProcessingMain(file_path, axis='z')

    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    height_lat = np.array(height_lat).astype(int)
    max_def_inches_lat = np.negative(max_def_inches_lat)

    sorted_indices_lat = np.argsort(height_lat)
    sorted_height_lat = height_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    regression_coefficients_lat = np.polyfit(sorted_height_lat, sorted_max_def_inches_lat, 2)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_height_lat)

    r2_lat = calc_r2(sorted_max_def_inches_lat, regression_curve_lat)

    fig.add_trace(go.Scatter(x=sorted_height_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_height_lat, y=regression_curve_lat, mode='lines',
                             name=f'Degree 2 Regression Curve Lateral {head}<br>r2 = {r2_lat: .4f}'))

