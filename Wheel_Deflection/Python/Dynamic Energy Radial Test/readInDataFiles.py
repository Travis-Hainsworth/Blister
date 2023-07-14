import numpy as np
import pandas as pd
import os
import re


def process_file_name(folder_dir, file):
    path = os.path.join(folder_dir, file.title())
    df = pd.read_csv(path, header=2, low_memory=False)

    file_parts = str(path).split('_')
    height = file_parts[7].split("Height")[1]
    head = file_parts[9][:4]
    rim = file_parts[4]

    df = df.drop(index=[0, 1])
    df = fix_mocap_df(df)
    df = df.drop(index=2)
    df.set_index('Frame', inplace=True)

    return df, height, rim, head


def get_mocap_data(folder_dir):
    files = sorted(os.listdir(folder_dir))
    combined_csvs, height = [], []
    rim, head = '', ''
    for file in files:
        df, hei, r, h = process_file_name(folder_dir, file)
        combined_csvs.append(df)
        height.append(hei)
        rim = r
        head = h

    return combined_csvs, height, rim, head


def fix_mocap_df(df):
    new_cols = {'Unnamed: 0': 'Frame', 'Name': 'Time (sec)'}
    first_row = df.iloc[0]
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
    displacements = []
    pattern_drop_head = r'^Unlabeled \d+\.\d+ Y$'
    degrees = [0, 45, 90, 135, 180, 225, 270, 315]

    for df in list_df:
        drop_head = [col for col in df.columns if re.match(pattern_drop_head, col)]
        drop_head_y = pd.to_numeric(df[drop_head[0]], errors='coerce')

        important_info = pd.DataFrame()
        important_info['drop_head_y'] = drop_head_y

        for degree in degrees:
            pattern_degree = r'^(RigidBody|Wheel1):Marker {}deg\.1 Y$'.format(degree)
            degree_cols = [col for col in df.columns if re.match(pattern_degree, col)]
            degree_y = pd.to_numeric(df[degree_cols[0]], errors='coerce')

            if degree == 0:
                if 'Wheel1:Marker 0deg.1 Y' in df.columns:
                    rim_top_y = pd.to_numeric(df['Wheel1:Marker 0deg.1 Y'], errors='coerce')
                    rim_hub_y = pd.to_numeric(df['Wheel1:Marker Hub.1 Y'], errors='coerce')
                else:
                    rim_top_y = pd.to_numeric(df['RigidBody:Marker 0deg.1 Y'], errors='coerce')
                    rim_hub_y = pd.to_numeric(df['RigidBody:Marker Hub.1 Y'], errors='coerce')

                displacement = np.abs(rim_hub_y - rim_top_y)
                max_displacement = displacement.min()
                scaled_displacement = max_displacement - displacement[0]
                displacements.append(scaled_displacement)

            displacement_degree = np.abs(rim_hub_y - degree_y)
            max_displacement_degree = displacement_degree.min()
            scaled_displacement_degree = max_displacement_degree - displacement_degree[0]
            important_info['displacement_{}deg'.format(degree)] = scaled_displacement_degree

        clean_list_df.append(important_info)

    return clean_list_df, displacements


""""
def clean_mocap_data(list_df):
    clean_list_df = []
    radial_deformations = []
    pattern_drop_head = r'^Unlabeled \d+\.\d+ Y$'
    degrees = [0, 45, 90, 135, 180, 225, 270, 315]

    for df in list_df:
        drop_head = [col for col in df.columns if re.match(pattern_drop_head, col)]
        drop_head_y = pd.to_numeric(df[drop_head[0]], errors='coerce')

        important_info = pd.DataFrame()
        important_info['drop_head_y'] = drop_head_y

        rim_marker_exists = True

        if 'Wheel1:Marker Hub.1 X' not in df.columns or \
           'Wheel1:Marker Hub.1 Y' not in df.columns or \
           'Wheel1:Marker Hub.1 Z' not in df.columns:
            rim_marker_exists = False
            continue  # Skip this DataFrame and move to the next iteration

        rim_center_x = pd.to_numeric(df['Wheel1:Marker Hub.1 X'], errors='coerce')
        rim_center_y = pd.to_numeric(df['Wheel1:Marker Hub.1 Y'], errors='coerce')
        rim_center_z = pd.to_numeric(df['Wheel1:Marker Hub.1 Z'], errors='coerce')

        for degree in degrees:
            pattern_degree_x = r'^(RigidBody|Wheel1):Marker {}deg\.1 X$'.format(degree)
            pattern_degree_y = r'^(RigidBody|Wheel1):Marker {}deg\.1 Y$'.format(degree)
            pattern_degree_z = r'^(RigidBody|Wheel1):Marker {}deg\.1 Z$'.format(degree)

            degree_cols_x = [col for col in df.columns if re.match(pattern_degree_x, col)]
            degree_cols_y = [col for col in df.columns if re.match(pattern_degree_y, col)]
            degree_cols_z = [col for col in df.columns if re.match(pattern_degree_z, col)]

            if degree_cols_x and degree_cols_y and degree_cols_z:
                degree_x = pd.to_numeric(df[degree_cols_x[0]], errors='coerce')
                degree_y = pd.to_numeric(df[degree_cols_y[0]], errors='coerce')
                degree_z = pd.to_numeric(df[degree_cols_z[0]], errors='coerce')

                if degree == 0:
                    initial_radius = np.sqrt((degree_x - rim_center_x)**2 + (degree_y - rim_center_y)**2 + (degree_z - rim_center_z)**2)

                current_radius = np.sqrt((degree_x - rim_center_x)**2 + (degree_y - rim_center_y)**2 + (degree_z - rim_center_z)**2)
                radial_deformation = current_radius - initial_radius

                important_info['radial_deformation_{}deg'.format(degree)] = radial_deformation

        clean_list_df.append(important_info)

    return clean_list_df, radial_deformations
"""

