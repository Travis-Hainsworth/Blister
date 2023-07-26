import plotly.graph_objects as go


def lateral_plot(defs, rims):
    fig = go.Figure()

    for i in range(len(defs)):
        fig.add_trace(go.Box(y=defs[i], name=rims[i]))

    fig.update_layout(
        title=f'Max Deformation per Trial {rims} head',
        xaxis=dict(title='Rims'),
        yaxis=dict(title='Deformation (mm)'),
        showlegend=True,
        font=dict(size=15)
    )

    fig.show()

