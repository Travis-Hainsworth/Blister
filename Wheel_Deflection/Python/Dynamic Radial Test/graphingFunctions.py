from dataProcessing import *
import plotly.graph_objects as go


# Plots the radial deformation with respect to the force for individual rims
def radial_plot_weight(file_path):
    max_defs, weight, _, rim, head = dataProcessingMain(file_path, axis='y')

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

    lateral_plot_weight(file_path, fig)

    fig.update_layout(
        title=f'Max Deformation per Trial {rim} {head} head',
        xaxis=dict(title='Force (lbf)'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15)
    )

    fig.show()


# Plots the radial deformation with respect to the drop height for individual rims
def radial_plot_height(file_path):
    max_defs, _, height, rim, head = dataProcessingMain(file_path, axis='y')

    max_def_inches = [i * .0393701 for i in max_defs]

    height = np.array(height).astype(int)
    max_def_inches = np.negative(max_def_inches)

    # Sort the data based on weight values
    sorted_indices = np.argsort(height)
    sorted_height = height[sorted_indices]
    sorted_max_def_inches = max_def_inches[sorted_indices]

    # Perform degree 2 polynomial regression
    regression_coefficients = np.polyfit(sorted_height, sorted_max_def_inches, 3)
    regression_curve = np.polyval(regression_coefficients, sorted_height)

    r2 = calc_r2(sorted_max_def_inches, regression_curve)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_height, y=sorted_max_def_inches, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_height, y=regression_curve, mode='lines',
                             name=f'Degree 2 Regression Curve Radial<br>r2 = {r2: .4f}'))

    lateral_plot_height(file_path, fig)

    fig.update_layout(
        title=f'Max Deformation per Trial {rim} {head} head',
        xaxis=dict(title='Drop Height'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15)
    )

    fig.show()


# Plots lateral deformation with respect to the force for individual rims
def lateral_plot_weight(file_path, fig):
    max_defs_lat, weight_lat, height_lat, _, head = dataProcessingMain(file_path, axis='z')

    weight_lat = np.array(weight_lat).astype(float)
    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    max_def_inches_lat = np.negative(max_def_inches_lat)
    sorted_indices_lat = np.argsort(weight_lat)

    sorted_weight_lat = weight_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    regression_coefficients_lat = np.polyfit(sorted_weight_lat, sorted_max_def_inches_lat, 3)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_weight_lat)

    r2_lat = calc_r2(sorted_max_def_inches_lat, regression_curve_lat)

    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_weight_lat, y=regression_curve_lat, mode='lines',
                             name=f'Degree 2 Regression Curve Lateral {head}<br>r2 = {r2_lat: .4f}'))


# Plots lateral deformation with respect to drop height for individual rims
def lateral_plot_height(file_path, fig):
    max_defs_lat, _, height_lat, _, head = dataProcessingMain(file_path, axis='z')

    max_def_inches_lat = [i * .0393701 for i in max_defs_lat]

    height_lat = np.array(height_lat).astype(int)
    max_def_inches_lat = np.negative(max_def_inches_lat)

    sorted_indices_lat = np.argsort(height_lat)
    sorted_height_lat = height_lat[sorted_indices_lat]
    sorted_max_def_inches_lat = max_def_inches_lat[sorted_indices_lat]

    regression_coefficients_lat = np.polyfit(sorted_height_lat, sorted_max_def_inches_lat, 3)
    regression_curve_lat = np.polyval(regression_coefficients_lat, sorted_height_lat)

    r2_lat = calc_r2(sorted_max_def_inches_lat, regression_curve_lat)

    fig.add_trace(go.Scatter(x=sorted_height_lat, y=sorted_max_def_inches_lat, mode='markers', marker=dict(size=8),
                             name=f'Test {head}'))
    fig.add_trace(go.Scatter(x=sorted_height_lat, y=regression_curve_lat, mode='lines',
                             name=f'Degree 2 Regression Curve Lateral {head}<br>r2 = {r2_lat: .4f}'))


# Plots all rims with the drop height on the x-axis
def comparison_plot_mean(max_defs, heights, rims, heads):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue', 'Lightblue', 'salmon']

    for i in range(len(max_defs)):
        sorted_max_def_inches, sorted_height = index_filtering(max_defs[i], heights[i])

        mean_values = [np.mean(sorted_max_def_inches[sorted_height == value]) for value in np.unique(sorted_height)]

        regression_curve, r2 = regression_helper(sorted_height, mean_values, 3, True)
        regression_curve_flat, r2_flat = regression_helper(sorted_height, mean_values, 1, True)

        if heads[i] == 'Flat':
            fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=regression_curve_flat,
                                     mode='lines', marker=dict(symbol='x'),
                                     line=dict(dash='dash', color=colors[counter - 1]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2_flat: .4f}'))
        elif heads[i] == 'Rock':
            fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=regression_curve,
                                     mode='lines', line=dict(color=colors[counter]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2: .4f}'))

        fig.update_layout(
            title='Max Deformation per Trial Radial Regression Curves',
            xaxis=dict(title='Drop Height'),
            yaxis=dict(title='Compression (in)'),
            showlegend=True,
            font=dict(size=15),
        )
        counter += 1
    fig.show()


# Plots all rims with a normalized force value on the x-axis
def comparison_plot_mean_weight(max_defs, weights, rims, heads):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue', 'Lightblue', 'salmon']

    for i in range(len(max_defs)):
        sorted_max_def_inches, sorted_weight = index_filtering(max_defs[i], weights[i])

        sorted_weight = (sorted_weight - np.min(sorted_weight)) / (np.max(sorted_weight) - np.min(sorted_weight))
        mean_values = [np.mean(sorted_max_def_inches[sorted_weight == value]) for value in np.unique(sorted_weight)]

        regression_curve, r2 = regression_helper(sorted_weight, mean_values, 3, True)
        regression_curve_flat, r2_flat = regression_helper(sorted_weight, mean_values, 1, True)

        if heads[i] == 'Flat':
            fig.add_trace(go.Scatter(x=np.unique(sorted_weight), y=regression_curve_flat,
                                     mode='lines', marker=dict(symbol='x'),
                                     line=dict(dash='dash', color=colors[counter - 1]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2_flat: .4f}'))
        elif heads[i] == 'Rock':
            fig.add_trace(go.Scatter(x=np.unique(sorted_weight), y=regression_curve,
                                     mode='lines', line=dict(color=colors[counter]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2: .4f}'))

        fig.update_layout(
            title='Max Deformation per Trial Radial Regression Curves',
            xaxis=dict(title='Normalized Force'),
            yaxis=dict(title='Compression (in)'),
            showlegend=True,
            font=dict(size=15)
        )
        counter += 1
    fig.show()


# Plots all rims based on if they are carbon or alloy
def carbon_vs_alloy_plot(max_defs, heights, rims, heads):
    fig = go.Figure()
    alloy_flat_means, alloy_rock_means, carbon_flat_means, carbon_rock_means = [], [], [], []

    for i in range(len(max_defs)):
        sorted_max_def_inches, sorted_height = index_filtering(max_defs[i], heights[i])

        mean_values = [np.mean(sorted_max_def_inches[sorted_height == value]) for value in np.unique(sorted_height)]

        if rims[i] == 'Stansflowmk4' or rims[i] == 'DTS':
            if heads[i] == 'Flat':
                alloy_flat_means.append(mean_values)
            else:
                alloy_rock_means.append(mean_values)
        elif heads[i] == 'Flat':
            carbon_flat_means.append(mean_values)
        else:
            carbon_rock_means.append(mean_values)

    alloy_flat_mean = array_means(alloy_flat_means)
    alloy_rock_mean = array_means(alloy_rock_means)

    carbon_flat_mean = array_means(carbon_flat_means)
    carbon_rock_mean = array_means(carbon_rock_means)

    alloy_flat_curve, alloy_flat_r2 = regression_helper(sorted_height, alloy_flat_mean, 1, True)
    alloy_rock_curve, alloy_rock_r2 = regression_helper(sorted_height, alloy_rock_mean, 3, True)

    carbon_flat_curve, carbon_flat_r2 = regression_helper(sorted_height, carbon_flat_mean, 1, True)
    carbon_rock_curve, carbon_rock_r2 = regression_helper(sorted_height, carbon_rock_mean, 3, True)

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=alloy_flat_curve,
                             mode='lines', line=dict(dash='dash', color='blue'),
                             name=f'Alloy Flat Head<br>r2 = {alloy_flat_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=alloy_rock_curve,
                             mode='lines', line=dict(color='blue'),
                             name=f'Alloy Rock Head<br>r2 = {alloy_rock_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=carbon_flat_curve,
                             mode='lines', line=dict(dash='dash', color='red'),
                             name=f'Carbon Flat Head<br>r2 = {carbon_flat_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=carbon_rock_curve,
                             mode='lines', line=dict(color='red'),
                             name=f'Carbon Rock Head<br>r2 = {carbon_rock_r2: .4f}'))

    fig.update_layout(
        title='Max Deformation per Trial Alloy vs. Carbon Radial Regression Curves',
        xaxis=dict(title='Drop Height'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15),
    )
    fig.show()


# Plots all rims based on the spoke count
def spoke_count_plot(max_defs, heights, rims, heads):
    fig = go.Figure()
    flat28_means, rock28_means, flat32_means, rock32_means = [], [], [], []

    for i in range(len(max_defs)):
        sorted_max_def_inches, sorted_height = index_filtering(max_defs[i], heights[i])

        mean_values = [np.mean(sorted_max_def_inches[sorted_height == value]) for value in np.unique(sorted_height)]

        if rims[i] == 'Stansflowmk4' or rims[i] == 'DTS' or rims[i] == 'Reserve30HD':
            if heads[i] == 'Flat':
                flat28_means.append(mean_values)
            else:
                rock28_means.append(mean_values)
        elif heads[i] == 'Flat':
            flat32_means.append(mean_values)
        else:
            rock32_means.append(mean_values)

    flat28_mean = array_means(flat28_means)
    rock28_mean = array_means(rock28_means)

    flat32_mean = array_means(flat32_means)
    rock32_mean = array_means(rock32_means)

    flat28_curve, flat28_r2 = regression_helper(sorted_height, flat28_mean, 3, True)
    rock28_curve, rock28_r2 = regression_helper(sorted_height, rock28_mean, 3, True)

    flat32_curve, flat32_r2 = regression_helper(sorted_height, flat32_mean, 3, True)
    rock32_curve, rock32_r2 = regression_helper(sorted_height, rock32_mean, 3, True)

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=flat28_curve,
                             mode='lines', line=dict(dash='dash', color='blue'),
                             name=f'Regression Curve Radial 28 Spokes Flat Head<br>r2 = {flat28_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=rock28_curve,
                             mode='lines', line=dict(color='blue'),
                             name=f'Regression Curve Radial 28 Spokes Rock Head<br>r2 = {rock28_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=flat32_curve,
                             mode='lines', line=dict(dash='dash', color='red'),
                             name=f'Regression Curve Radial 32 Spokes Flat Head<br>r2 = {flat32_r2: .4f}'))

    fig.add_trace(go.Scatter(x=np.unique(sorted_height), y=rock32_curve,
                             mode='lines', line=dict(color='red'),
                             name=f'Regression Curve Radial 32 Spokes Rock Head<br>r2 = {rock32_r2: .4f}'))

    fig.update_layout(
        title='Max Deformation per Trial Spoke Count',
        xaxis=dict(title='Drop Height'),
        yaxis=dict(title='Compression (in)'),
        showlegend=True,
        font=dict(size=15),
    )
    fig.show()


# Plots all rims with force on the x-axis and height on the y-axis
def comparison_plot_weight_height(max_defs, weights, heights, rims, heads):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue', 'Lightblue', 'salmon']

    for i in range(len(max_defs)):
        sorted_max_def_inches, sorted_weight = index_filtering(max_defs[i], weights[i])
        holder, sorted_height = index_filtering(max_defs[i], heights[i])

        mean_values = [np.mean(sorted_weight[sorted_weight == value]) for value in sorted_weight]

        regression_curve, r2 = regression_helper(mean_values, sorted_height, 3, False)
        regression_curve_flat, r2_flat = regression_helper(mean_values, sorted_height, 2, False)

        if heads[i] == 'Flat':
            fig.add_trace(go.Scatter(x=mean_values, y=regression_curve_flat,
                                     mode='lines', marker=dict(symbol='x'),
                                     line=dict(dash='dash', color=colors[counter - 1]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2_flat: .4f}'))
        elif heads[i] == 'Rock':
            fig.add_trace(go.Scatter(x=mean_values, y=regression_curve,
                                     mode='lines', line=dict(color=colors[counter]),
                                     name=f'{rims[i]} {heads[i]}<br>r2 = {r2: .4f}'))

        fig.update_layout(
            title='Max Deformation per Trial Radial Regression Curves',
            xaxis=dict(title='Force'),
            yaxis=dict(title='Drop Height'),
            showlegend=True,
            font=dict(size=15)
        )
        counter += 1
    fig.show()