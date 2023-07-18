from dataProcessing import *
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer


def plot_all_markers(lists, rims, heads):
    x_values = np.arange(0, 100, 10)
    fig = go.Figure()

    # Loop through each column and create individual plots
    for i in range(len(lists)):
        fig.add_trace(go.Scatter(x=x_values, y=lists[i], mode='lines', name=f'{rims[i][0]} {heads[i][0]}'))
    fig.show()


def percent_diff_plot(energy_diffs, drop_heights, rims, heads):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'aqua', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue',
              'Lightblue', 'salmon']

    for i in range(len(energy_diffs)):

        sorted_percent_diffs, sorted_drop_heights = index_filtering(energy_diffs[i], drop_heights[i])

        # Preprocess the data
        sorted_percent_diffs, sorted_drop_heights = preprocess_data(sorted_percent_diffs, sorted_drop_heights)

        if len(sorted_percent_diffs) == 0 or len(sorted_drop_heights) == 0:
            continue

        # Find the best degree for the polynomial regression
        best_degree = find_best_degree(sorted_drop_heights, sorted_percent_diffs, [1])

        # Fit the polynomial regression model
        poly_features = PolynomialFeatures(degree=best_degree)
        X_poly = poly_features.fit_transform(sorted_drop_heights.reshape(-1, 1))
        model = LinearRegression()
        model.fit(X_poly, sorted_percent_diffs)
        regression_curve = model.predict(X_poly)

        this_color = colors[i]
        if rims[i][0] == rims[i - 1][0]:
            this_color = colors[i - 1]
            fig.add_trace(go.Scatter(x=sorted_drop_heights, y=regression_curve, mode='lines',
                                     name=f'{rims[i][0]} {heads[i][0]}', line=dict(color=this_color)))
        else:
            fig.add_trace(go.Scatter(x=sorted_drop_heights, y=regression_curve, mode='lines',
                                     name=f'{rims[i][0]} {heads[i][0]}',
                                     line=dict(dash='dash', color=this_color)))

        counter += 1

    fig.update_layout(
        title=f'Energy Absorbed vs. Drop Heights Regression Lines, n=62',
        xaxis=dict(title=f'Drop Height'),
        yaxis=dict(title='Energy Absorbed (J)'),
        showlegend=True,
        font=dict(size=15)
    )
    fig.show()


def height_vs_displacement(height, displacement, rims, heads):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'aqua', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue',
              'Lightblue', 'salmon']

    for i in range(len(height)):
        sorted_defs, sorted_drop_heights = index_filtering(displacement[i], height[i])

        # Preprocess the data
        sorted_defs, sorted_drop_heights = preprocess_data(sorted_defs, sorted_drop_heights)

        if len(sorted_defs) == 0 or len(sorted_drop_heights) == 0:
            continue

        # Preprocess the data
        sorted_defs, sorted_drop_heights = preprocess_data(sorted_defs, sorted_drop_heights)

        if len(sorted_defs) == 0 or len(sorted_drop_heights) == 0:
            continue

        # Find the best degree for the polynomial regression
        best_degree = find_best_degree(sorted_drop_heights, sorted_defs, [1, 2, 3, 4])

        # Fit the polynomial regression model
        poly_features = PolynomialFeatures(degree=best_degree)
        X_poly = poly_features.fit_transform(sorted_drop_heights.reshape(-1, 1))
        model = LinearRegression()
        model.fit(X_poly, sorted_defs)
        regression_curve = model.predict(X_poly)
        this_color = colors[i]

        if rims[i][0] == rims[i - 1][0]:
            this_color = colors[i - 1]
            fig.add_trace(go.Scatter(x=sorted_drop_heights, y=regression_curve, mode='lines',
                                     name=f'{rims[i][0]} {heads[i][0]}', line=dict(color=this_color)))

        else:
            fig.add_trace(go.Scatter(x=sorted_drop_heights, y=regression_curve,
                                     name=f'{rims[i][0]} {heads[i][0]}',
                                     line=dict(dash='dash', color=this_color)))

        counter += 1

    fig.update_layout(
        title=f'Displacement vs. Drop Height Regression Lines, n=62',
        xaxis=dict(title=f'Drop Height'),
        yaxis=dict(title='Displacement (in)'),
        showlegend=True,
        font=dict(size=15)
    )
    fig.show()


def energy_vs_displacement(energy, displacement, rims, heads, norm=False):
    counter = 0
    fig = go.Figure()
    colors = ['Red', 'Blue', 'Green', 'aqua', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue',
              'Lightblue', 'salmon']

    for i in range(len(energy)):
        sorted_defs, sorted_energy = index_filtering(displacement[i], energy[i])

        # Preprocess the data
        sorted_energy, sorted_defs = preprocess_data(sorted_energy, sorted_defs)

        if len(sorted_defs) == 0 or len(sorted_energy) == 0:
            continue

        if norm:
            sorted_energy = (sorted_energy - np.min(sorted_energy)) / (np.max(sorted_energy) - np.min(sorted_energy))

        # Find the best degree for the polynomial regression
        best_degree = find_best_degree(sorted_energy, sorted_defs, [1, 2, 3, 4])

        # Fit the polynomial regression model
        poly_features = PolynomialFeatures(degree=best_degree)
        X_poly = poly_features.fit_transform(sorted_energy.reshape(-1, 1))
        model = LinearRegression()
        model.fit(X_poly, sorted_defs)
        regression_curve = model.predict(X_poly)

        this_color = colors[i]
        if rims[i][0] == rims[i - 1][0]:
            this_color = colors[i - 1]
            fig.add_trace(go.Scatter(x=sorted_energy, y=regression_curve,
                                     name=f'{rims[i][0]} {heads[i][0]}', line=dict(color=this_color)))

        else:
            fig.add_trace(go.Scatter(x=sorted_energy, y=regression_curve,
                                     name=f'{rims[i][0]} {heads[i][0]}', line=dict(dash='dash', color=this_color)))

        counter += 1

    fig.update_layout(
        title=f'Energy Absorbed vs. Displacement Regression Lines, n=62',
        xaxis=dict(title=f'Normalized Energy Absorbed (J)'),
        yaxis=dict(title='Displacement (in)'),
        showlegend=True,
        font=dict(size=15)
    )
    fig.show()


# def energy_vs_energy(energy_dif, displacement, rims, heads, norm=False):
#     counter = 0
#     fig = go.Figure()
#     colors = ['Red', 'Blue', 'Green', 'aqua', 'Purple', 'Black', 'Orange', 'Pink', 'aqua', 'Brown', 'Darkblue',
#               'Lightblue', 'salmon']
#
#     for i in range(len(energy)):
#         sorted_defs, sorted_energy = index_filtering(displacement[i], energy[i])
#
#         # Preprocess the data
#         sorted_energy, sorted_defs = preprocess_data(sorted_energy, sorted_defs)
#
#         if len(sorted_defs) == 0 or len(sorted_energy) == 0:
#             continue
#
#         if norm:
#             sorted_energy = (sorted_energy - np.min(sorted_energy)) / (np.max(sorted_energy) - np.min(sorted_energy))
#
#         # Find the best degree for the polynomial regression
#         best_degree = find_best_degree(sorted_energy, sorted_defs, [1, 2, 3, 4])
#
#         # Fit the polynomial regression model
#         poly_features = PolynomialFeatures(degree=best_degree)
#         X_poly = poly_features.fit_transform(sorted_energy.reshape(-1, 1))
#         model = LinearRegression()
#         model.fit(X_poly, sorted_defs)
#         regression_curve = model.predict(X_poly)
#
#         this_color = colors[i]
#         if rims[i][0] == rims[i - 1][0]:
#             this_color = colors[i - 1]
#             fig.add_trace(go.Scatter(x=sorted_energy, y=regression_curve,
#                                      name=f'{rims[i][0]} {heads[i][0]}', line=dict(color=this_color)))
#
#         else:
#             fig.add_trace(go.Scatter(x=sorted_energy, y=regression_curve,
#                                      name=f'{rims[i][0]} {heads[i][0]}', line=dict(dash='dash', color=this_color)))
#
#         counter += 1
#
#     fig.update_layout(
#         title=f'Energy vs. Displacement',
#         xaxis=dict(title=f'Normalized Energy (J)'),
#         yaxis=dict(title='Displacement (in)'),
#         showlegend=True,
#         font=dict(size=15)
#     )
#     fig.show()


def preprocess_data(X, y):
    # Remove NaN, infinity, and large values
    mask = np.isfinite(X) & np.isfinite(y)
    X_clean = X[mask]
    y_clean = y[mask]

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X_clean.reshape(-1, 1))
    y_imputed = imputer.fit_transform(y_clean.reshape(-1, 1))

    return X_imputed.flatten(), y_imputed.flatten()


def find_best_degree(X, y, degrees):
    best_degree = None
    best_score = -np.inf

    for degree in degrees:
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X.reshape(-1, 1))
        model = LinearRegression()
        scores = cross_val_score(model, X_poly, y, cv=5, scoring='r2')
        avg_score = np.mean(scores)

        if avg_score > best_score:
            best_score = avg_score
            best_degree = degree

    return best_degree
