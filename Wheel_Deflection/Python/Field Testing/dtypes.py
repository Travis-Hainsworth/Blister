# Holder for dtype readings in readInDataFiles.py
dtype_dict = {
    'Time (sec)': 'float32',
    'Unlabeled 3702.1 Y': 'float32',
    'Unlabeled 3702.1 Z': 'float32',
    'Wheel1:Marker 0deg.1 Y': 'float32',
    'Wheel1:Marker 0deg.1 Z': 'float32',
    'Wheel1:Marker 0deg.1 X': 'float32',
    'Wheel1:Marker 135deg.1 Y': 'float32',
    'Wheel1:Marker 135deg.1 Z': 'float32',
    'Wheel1:Marker 135deg.1 X': 'float32',
    'Wheel1:Marker 180deg.1 Y': 'float32',
    'Wheel1:Marker 180deg.1 Z': 'float32',
    'Wheel1:Marker 180deg.1 X': 'float32',
    'Wheel1:Marker 225deg.1 Y': 'float32',
    'Wheel1:Marker 225deg.1 Z': 'float32',
    'Wheel1:Marker 225deg.1 X': 'float32',
    'Wheel1:Marker 270deg.1 Y': 'float32',
    'Wheel1:Marker 270deg.1 Z': 'float32',
    'Wheel1:Marker 270deg.1 X': 'float32',
    'Wheel1:Marker 315deg.1 Y': 'float32',
    'Wheel1:Marker 315deg.1 Z': 'float32',
    'Wheel1:Marker 315deg.1 X': 'float32',
    'Wheel1:Marker 45deg.1 Y': 'float32',
    'Wheel1:Marker 45deg.1 Z': 'float32',
    'Wheel1:Marker 45deg.1 X': 'float32',
    'Wheel1:Marker 90deg.1 Y': 'float32',
    'Wheel1:Marker 90deg.1 Z': 'float32',
    'Wheel1:Marker 90deg.1 X': 'float32',
    'Wheel1:Marker Hub.1 Y': 'float32',
    'Wheel1:Marker Hub.1 X': 'float32',
    'Wheel1:Marker Hub.1 Z': 'float32',
    'RigidBody:Marker 0deg.1 Y': 'float32',
    'RigidBody:Marker 0deg.1 Z': 'float32',
    'RigidBody:Marker 0deg.1 X': 'float32',
    'RigidBody:Marker 135deg.1 Y': 'float32',
    'RigidBody:Marker 135deg.1 Z': 'float32',
    'RigidBody:Marker 135deg.1 X': 'float32',
    'RigidBody:Marker 180deg.1 Y': 'float32',
    'RigidBody:Marker 180deg.1 Z': 'float32',
    'RigidBody:Marker 180deg.1 X': 'float32',
    'RigidBody:Marker 225deg.1 Y': 'float32',
    'RigidBody:Marker 225deg.1 Z': 'float32',
    'RigidBody:Marker 225deg.1 X': 'float32',
    'RigidBody:Marker 270deg.1 Y': 'float32',
    'RigidBody:Marker 270deg.1 Z': 'float32',
    'RigidBody:Marker 270deg.1 X': 'float32',
    'RigidBody:Marker 315deg.1 Y': 'float32',
    'RigidBody:Marker 315deg.1 Z': 'float32',
    'RigidBody:Marker 315deg.1 X': 'float32',
    'RigidBody:Marker 45deg.1 Y': 'float32',
    'RigidBody:Marker 45deg.1 Z': 'float32',
    'RigidBody:Marker 45deg.1 X': 'float32',
    'RigidBody:Marker 90deg.1 Y': 'float32',
    'RigidBody:Marker 90deg.1 Z': 'float32',
    'RigidBody:Marker 90deg.1 X': 'float32',
    'RigidBody:Marker Hub.1 Y': 'float32',
    'RigidBody:Marker Hub.1 X': 'float32',
    'RigidBody:Marker Hub.1 Z': 'float32'
}

wheel_pattern_y = r'^Wheel:Marker\d+\.\d+ Y$'
hub_pattern_y = r'^Hub\.4 Y$'
wheel_pattern_x = r'^Wheel:Marker\d+\.\d+ X$'
hub_pattern_x = r'^Hub\.4 X$'
wheel_pattern_z = r'^Wheel:Marker\d+\.\d+ Z$'
hub_pattern_z = r'^Hub\.4 Z$'

wheel_pattern_y_col = r'^wheel_y_.*'
hub_pattern_y_col = r'^hub_y_.*'
wheel_pattern_x_col = r'^wheel_x_.*'
hub_pattern_x_col = r'^hub_x_.*'
wheel_pattern_z_col = r'^wheel_z_.*'
hub_pattern_z_col = r'^hub_z_.*'

