import plotly.graph_objects as go
import numpy as np
import pandas as pd


# Plots the lateral deformation vs the load  found from the mts,
def plot_lateral_deformations(mocap_datasets, mts_datasets, rims):
    fig = go.Figure()

    for i, (mocap, mts) in enumerate(zip(mocap_datasets, mts_datasets)):
        all_lines = []

        for j in range(len(mocap)):
            # Convert 'time' column in mocap to timedelta
            mocap[j]['Time (sec)'] = pd.to_timedelta(mocap[j]['Time (sec)'].astype(float), unit='s')

            # Resample mocap data to match the time points of mts data
            resampled_mocap = mocap[j].set_index('Time (sec)').resample('1s').mean()

            # Interpolate 'Load (lbf)' to match the time points of resampled mocap data
            interp_load = np.interp(
                np.linspace(0, 200, num=200),
                mts[j]['Time (sec)'].astype(float),
                mts[j]['Load (lbf)'].astype(float),
            )

            # Store individual line
            line = np.linspace(resampled_mocap['rim_y'].iloc[0], max(resampled_mocap['rim_y']), len(interp_load))
            all_lines.append(line)

        # Calculate the mean line and the padded lines for the current dataset
        max_len = max(len(line) for line in all_lines)

        all_lines_padded = [line.tolist() + [line[-1]] * (max_len - len(line)) for line in all_lines]

        mean_line = np.mean(all_lines_padded, axis=0)
        std_dev_line = np.std(all_lines_padded, axis=0)

        legend_name = f'Mean Line ± Standard Deviation ({rims[i]})'

        # Plot the mean line and the shaded error bar for the current dataset
        fig.add_trace(go.Scatter(
            x=np.arange(len(mean_line)),
            y=mean_line,
            line=dict(width=1),
            name=legend_name
        ))

        fig.add_trace(go.Scatter(
            x=np.arange(len(mean_line)),
            y=mean_line - (2 * std_dev_line),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=np.arange(len(mean_line)),
            y=mean_line + (2 * std_dev_line),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))

    fig.update_layout(
        xaxis_title='Load (lbf)',
        yaxis_title='Displacement (mm)',
        title='Lateral Deformation n=25',
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        ),
        margin=dict(l=50, r=20, t=80, b=50),
        template='plotly_white',
        xaxis_range=[0, 200]
    )

    fig.show()
