# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:27:26 2024

@author: Vutara
"""

import json

import numpy as np

# Example usage
start_position = [-1516,583,-2049.6]  # Initial position (x,y,z) everything is is um 
x_range = 1
y_range = 25
z_range = 1
step_size_x = 1
step_size_y = 0.40
step_size_z = 1
constant_stage_port = 31

shifted_pos = np.zeros(3)
shifted_pos[0] = start_position[0] - x_range / 2
shifted_pos[1] = start_position[1] #-  y_range / 2
shifted_pos[2] = start_position[2]  



def generate_positions(start_pos, x_range, y_range, z_range):
    positions_array = []
    position_count = 0

    x_start, y_start, z_start = shifted_pos

    for z_step in range(int(z_range / step_size_z)):
        z = z_start - z_step * step_size_z
        for y_step in range(int(y_range / step_size_y)):
#            y = y_start + y_step * step_size_y     # stage moving up 
            y = y_start - y_step * step_size_y     # stage moving down    
            for x_step in range(int(x_range / step_size_x)):
                x = x_start + x_step * step_size_x
#                x = x_start - x_step * step_size_x
                
                # Create position dictionary
                position = {
                    "DefaultXYStage": {"type": "STRING", "scalar": f"XYStage:XY:{constant_stage_port}"},
                    "DefaultZStage": {"type": "STRING", "scalar": "ZStage:Z:32"},
                    "DevicePositions": {
                        "type": "PROPERTY_MAP",
                        "array": [
                            {
                                "Device": {"type": "STRING", "scalar": "ZStage:Z:32"},
                                "Position_um": {"type": "DOUBLE", "array": [z]}
                            },
                            {
                                "Device": {"type": "STRING", "scalar": f"XYStage:XY:{constant_stage_port}"},
                                "Position_um": {"type": "DOUBLE", "array": [x, y]}
                            }
                        ]
                    },
                    "Label": {"type": "STRING", "scalar": f"Pos{position_count}"}
                }
                positions_array.append(position)
                position_count += 1

    # Create the final JSON structure
    print(position_count)
    return {
        "encoding": "UTF-8",
        "format": "Micro-Manager Property Map",
        "major_version": 2,
        "minor_version": 0,
        "map": {
            "StagePositions": {
                "type": "PROPERTY_MAP",
                "array": positions_array
            }
        }
    }

# Generate positions and write to file
positions_data = generate_positions(start_position, x_range, y_range, z_range)
positions_json = json.dumps(positions_data, separators=(',', ':'))  # Compact JSON
filename = "micromanager_positions_optimized.pos"


with open(filename, "w") as f:
    f.write(positions_json)

print(f"Micro-Manager positions have been written to {filename}")