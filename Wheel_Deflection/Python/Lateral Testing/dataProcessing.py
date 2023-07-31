from readInDataFiles import *


# Helper function for file reading. Make sure to change the file paths to match your file path.
# Keep the file paths consistent, so you only need the rim name for it to work.
def process_lateral_data(rims):
    mocap_data = []
    mts_data = []

    for rim in rims:
        mocap_data.append(get_mocap_data(r"C:\Users\ethan\Test\Static_Lateral\{}\MOCAP".format(rim)))
        mts_data.append(get_mts_data(r"C:\Users\ethan\Test\Static_Lateral\{}\MTS".format(rim)))

    return mocap_data, mts_data
