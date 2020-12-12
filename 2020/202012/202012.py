# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 08:19:49 2020

@author: kbasa
"""

import numpy as np

with open("input.txt") as f:
    p_in = f.read().splitlines()

move_dict = {"W": np.intp((0, -1)),
             "N": np.intp((-1, 0)),
             "E": np.intp((0, 1)),
             "S": np.intp((1, 0))
             }

def move_ship(pos: np.ndarray, heading: np.intp, command: str) -> tuple:
    global move_dict
    com_dir, com_val = command[0], int(command[1:])

    if com_dir in "RL":
        com_rad = np.deg2rad(com_val) * (-1 if "R" in com_dir else 1)
        trans_matrix = np.array([[np.cos(com_rad), -np.sin(com_rad)],
                                 [np.sin(com_rad), np.cos(com_rad)]])
        new_heading = np.matmul(trans_matrix, heading)
        movement = np.intp([0, 0])

    elif com_dir == "F":
        new_heading = heading
        movement = new_heading * com_val

    elif com_dir in "WESN":
        new_heading = heading
        movement = move_dict[com_dir] * com_val

    return pos + movement, new_heading


state = []
pos, heading = np.intp([0, 0]), np.intp([0, 1])
for command in p_in:
    pos, heading = move_ship(pos, heading, command)
    state.append([command, tuple(pos), tuple(heading)])

print(f"Part 1 coordinates' sum is: {np.sum(np.abs(pos))}")


# %% Part 2
def move_with_wp(pos: np.intp, wp: np.intp, command: str) -> tuple:
    global move_dict
    com_dir, com_val = command[0], int(command[1:])

    if com_dir == "F":
        movement = wp * com_val
        new_pos = pos + movement
        new_wp = wp

    elif com_dir in "RL":
        com_rad = np.deg2rad(com_val) * (-1 if "R" in com_dir else 1)
        trans_matrix = np.array([[np.cos(com_rad), -np.sin(com_rad)],
                                 [np.sin(com_rad), np.cos(com_rad)]])
        new_wp = np.matmul(trans_matrix, wp)
        new_pos = pos

    elif com_dir in "WESN":
        new_pos = pos
        new_wp = wp + move_dict[com_dir] * com_val

    return new_pos, new_wp


state_p2 = []
pos, wp = np.intp([0, 0]), np.intp([-1, 10])
for command in p_in:
    pos, wp = move_with_wp(pos, wp, command)
    state_p2.append([command, tuple(pos), tuple(wp)])

print(f"Part 2 coordinates' sum is: {np.sum(np.abs(pos))}")
