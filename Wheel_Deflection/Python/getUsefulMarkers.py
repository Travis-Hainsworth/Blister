"""
Get the indecies of the columns that pertain to the specific markers...
MTS head, top of the rim, and the center of the axel. Could be added upon
to include other points of interst.

Input:
mocap_synced = trimmed data from the motion capture
i = index of the MTS head column
rim_top = the index of the rimtop y-axis indicator
center = the index of the center y- axis indicator

Output:
mo_time = the time column from the mocap_synced
m_head = the columns pretaining to the head indicator
m_rim_top = the columns pretaining to the rim top indicator
x_axle = the columns pretaining to the axel indicator
"""


def get_useful_markers(mocap_synced, i, rim_top, center):
    mo_time = mocap_synced.iloc[:, 2]

    m_head = mocap_synced.iloc[:, i-1:i+1]

    m_rim_top = mocap_synced.iloc[:, rim_top-1:rim_top+1]
    m_axle = mocap_synced.iloc[:,center-1:center+1]

    return mo_time, m_head, m_rim_top, m_axle
