import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors


def plot_results(energy, displacement, show=True):
    rims = ['Dtswissm1900', 'Enveam30', 'Lighten928', 'Reserve30Hd', 'Stansflowmk4', 'Waou']
    means_energy = []
    means_def = []
    best_rims = []

    # Calculate means for each rim and store them in lists
    for i in range(len(rims)):
        sorted_energy = np.loadtxt(f"energy{rims[i]}.txt")
        sorted_defs = np.loadtxt(f"defs{rims[i]}.txt")

        mean_energy = np.mean(sorted_energy, axis=0)
        mean_defs = np.mean(sorted_defs, axis=0)

        means_energy.append(mean_energy)
        means_def.append(mean_defs)

    # Normalize the means
    norm_e = (means_energy - np.min(means_energy)) / (np.max(means_energy) - np.min(means_energy))
    norm_d = (means_def - np.min(means_def)) / (np.max(means_def) - np.min(means_def))

    # Create a list to store normalized data and rim identifiers
    normalized_data = []
    rim_identifiers = []

    # Store normalized data and rim identifiers in the lists
    for i in range(len(rims)):
        normalized_data.append((norm_e[i], norm_d[i]))
        rim_identifiers.append(rims[i])

    # Create the scatter plot
    fig = go.Figure()

    for i in range(len(normalized_data)):
        rim_id = rim_identifiers[i]
        norm_e_val, norm_d_val = normalized_data[i]

        fig.add_trace(go.Scatter(x=[norm_e_val], y=[norm_d_val], mode='markers', name=rim_id))

    fig.add_trace(go.Scatter(x=[energy], y=[displacement], mode='markers', name='results'))

    arr = np.array(normalized_data)
    n_neighbors = 2

    knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto')
    knn.fit(arr)
    _, indices = knn.kneighbors([[energy, displacement]])

    for idx in indices[0]:
        neighbor_id = rim_identifiers[idx]
        neighbor_norm_e_val, neighbor_norm_d_val = normalized_data[idx]
        fig.add_trace(go.Scatter(x=[neighbor_norm_e_val], y=[neighbor_norm_d_val], mode='markers', marker=dict(symbol='x', size=12), name=f'{neighbor_id} (Best Rim)'))
        best_rims.append(neighbor_id)

    if show:
        fig.update_layout(
            title=f'Energy Absorbed vs. Displacement Regression Lines',
            xaxis=dict(title=f'Normalized Energy Absorbed (J)'),
            yaxis=dict(title='Normalized Displacement (in)'),
            showlegend=True,
            font=dict(size=15)
        )
        fig.show()

    return best_rims

