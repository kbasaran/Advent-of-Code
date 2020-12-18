# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:29:51 2020

@author: kbasa
"""

import numpy as np
from itertools import product
import time

start = time.time()

with open("input.txt") as f:
    p_in = f.read().splitlines()

n_d = 4
turns = 6

edge_size = len(p_in) + 2 + turns * 2
space = np.full([edge_size] * n_d, False, dtype=bool)
new_space = np.array(space, copy=True)
origin = np.array([int(edge_size / 2 - len(p_in) / 2 + 1)] * n_d)

# Makes coordinates of neighbours for use with numpy advanced indexing
neighbour_mask = list(product([-1, 0, 1], repeat=n_d))
neighbour_mask.remove(tuple([0] * n_d))
neig_mask_per_dim = []  # list of values for each coordinate
for dim in range(n_d):
    neig_mask_per_dim.append(np.array([i[dim] for i in neighbour_mask]))


def count_active_neighbours(pos):
    global space
    if (0 in pos) or ((edge_size - 1) in pos):
        # On the edge
        return 0

    neig_pos_per_dim = []
    for dim in range(n_d):
        neig_pos_per_dim.append(pos[dim] + neig_mask_per_dim[dim])
    neig_pos_per_dim = tuple(neig_pos_per_dim)

    return np.count_nonzero(space[neig_pos_per_dim] == True)


# Apply the game rules
def analyze(pos):
    global space
    act_neighb_count = count_active_neighbours(pos)
    me = space[pos]
    if me & (not (2 <= act_neighb_count <= 3)):
        return False
    elif (not me) & (act_neighb_count == 3):
        return True
    else:
        return me


# Run simultaneously on all positions.
def update_simul_all():
    global space, new_space
    new_space = np.array(space, copy=True)
    for pos in np.ndindex(space.shape):
        new_space[pos] = analyze(pos)
    space = new_space


# Translate the puzzle input file into the ndarray
for i, i_val in enumerate(p_in):
    for j, ij_val in enumerate(i_val):
        if ij_val == "#":
            space[tuple(origin + tuple([0] * (n_d - 2) + [i, j]))] = True


# Iterate through the turns
for i in range(turns):
    update_simul_all()
    print()
    print(f"Turn: {i+1}, Array size: {space.size * space.itemsize / 2**20:.3g} MB")
    print(f"Time: {time.time()-start:.4g}s, Count of active cells: {np.sum(space)}")
