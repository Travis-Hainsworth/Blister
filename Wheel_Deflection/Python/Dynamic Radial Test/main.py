import numpy as np
from dampingAnalysisMain import dataProcessingMain, onclick
import plotly.graph_objects as go

mocap, fftData, max_defs, weight = dataProcessingMain(r"C:\Users\ethan\Test\Dynamic_Testing\Light\Testing Round 1", plot=False)
max_def_inches = [i * .0393701 for i in max_defs]

weight = np.array(weight).astype(float)
max_def_inches = np.negative(max_def_inches)

fig = go.Figure()
fig.add_trace(go.Scatter(x=weight, y=max_def_inches, mode='lines'))

fig.update_layout(
    title='Max Deformation per Trial',
    xaxis=dict(title='Force (klbf)', tickmode='linear', tick0=0, dtick=100),
    yaxis=dict(title='Compression (in)'),
    showlegend=False
)

fig.show()


# threshold = 0.02  # Adjust this threshold value as per your requirement
# settling_time = find_settling_time(fftData, threshold)
