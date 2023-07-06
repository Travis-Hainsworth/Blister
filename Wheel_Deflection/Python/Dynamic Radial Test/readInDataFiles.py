import pandas as pd
import numpy as np
from os import listdir


def get_mocap_data(folder_dir):
    files = sorted(listdir(folder_dir))
    combined_csvs, weight, height = [], [], []
    rim, head = '', ''

    for file in files:
        path = f"{folder_dir}/{file.title()}"
        df = pd.read_csv(path, header=2, low_memory=False)

        weight.append(str(path).split('_')[9].split('Lbf')[0][-4:])
        height.append(str(path).split('_')[7].split("Height")[1])
        rim = str(path).split('_')[5]
        head = str(path).split('_')[3][:4]

        df = df.drop(index=[0, 1])
        df = fix_mocap_df(df)
        df = df.drop(index=2)
        df.set_index('Frame', inplace=True)

        combined_csvs.append(df)

    return combined_csvs, weight, height, rim, head


def fix_mocap_df(df):
    new_cols = {'Unnamed: 0': 'Frame', 'Name': 'Time (sec)'}
    first_row = np.array(df.iloc[0])
    marker_name = ""

    for count, col in enumerate(df.columns):
        if count >= 2:
            if count % 3 == 0:
                marker_name = col
            new_cols[col] = marker_name + " " + first_row[count]

    df = df.rename(columns=new_cols, errors="raise")
    return df


def clean_mocap_data(list_df):
    clean_list_df = []
    # Find the MTS head column
    for df in list_df:
        # Getting all the y values of each marker and finding the max
        first_row = df.iloc[0]
        y_vals = first_row[2::3].astype(float)

        max_y = max(y_vals)

        # Labeling the columns corresponding to the rim top marker
        for index in y_vals.index:
            if y_vals[index] == max_y:
                # Rim Top Y Column -> rimTopY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'rim_top_y'}, inplace=True)
                df.rename(columns={df.columns[num_index - 1]: 'rim_top_x'}, inplace=True)
                df.rename(columns={df.columns[num_index + 1]: 'rim_top_z'}, inplace=True)
                y_vals = y_vals.drop(index)

        # recalculate max to find axel column
        max_y = max(y_vals)

        for index in y_vals.index:
            if y_vals[index] == max_y:
                # Axel Top Y Column -> axelY
                num_index = df.columns.get_loc(index)
                df.rename(columns={df.columns[num_index]: 'axel_y'}, inplace=True)
                df.rename(columns={df.columns[num_index - 1]: 'axel_x'}, inplace=True)
                df.rename(columns={df.columns[num_index + 1]: 'axel_z'}, inplace=True)
                y_vals = y_vals.drop(index)

        # Re-labelling the xyz columns of the stand marker
        num_index = df.columns.get_loc(y_vals.index[0])
        df.rename(columns={df.columns[num_index]: 'stand_y'}, inplace=True)
        df.rename(columns={df.columns[num_index - 1]: 'stand_x'}, inplace=True)
        df.rename(columns={df.columns[num_index + 1]: 'stand_z'}, inplace=True)

        # finds original distance between the stand and rim markers
        first_row = df.iloc[0]

        rim_to_stand = {}

        rim_to_stand_x = float(first_row['rim_top_x']) - float(first_row['stand_x'])
        rim_to_stand["x"] = rim_to_stand_x

        rim_to_stand_y = float(first_row['rim_top_y']) - float(first_row['stand_y'])
        rim_to_stand["y"] = rim_to_stand_y

        rim_to_stand_z = float(first_row['rim_top_z']) - float(first_row['stand_z'])
        rim_to_stand["z"] = rim_to_stand_z

        # Converting these columns to have type float
        df['rim_top_x'] = pd.to_numeric(df['rim_top_x'], errors='coerce')
        df['rim_top_y'] = pd.to_numeric(df['rim_top_y'], errors='coerce')
        df['rim_top_z'] = pd.to_numeric(df['rim_top_z'], errors='coerce')
        df['stand_x'] = pd.to_numeric(df['stand_x'], errors='coerce')
        df['stand_y'] = pd.to_numeric(df['stand_y'], errors='coerce')
        df['stand_z'] = pd.to_numeric(df['stand_z'], errors='coerce')
        df['Time (sec)'] = pd.to_numeric(df['Time (sec)'], errors='coerce')

        """"
        first finds the distance between the stand and rim for each point in time
        and subtracts the original distance to filter out noise from the stand
        moving due to the carrige and piston catch
        """

        df['Displacementx'] = rim_to_stand["x"] - (df['rim_top_x'] - df['stand_x'])
        df['Displacementy'] = rim_to_stand["y"] - (df['rim_top_y'] - df['stand_y'])
        df['Displacementz'] = rim_to_stand["z"] - (df['rim_top_z'] - df['stand_z'])

        clean_list_df.append(df)

    return clean_list_df

