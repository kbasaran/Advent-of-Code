# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
# with open("test2.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import pandas as pd
import scipy.sparse.csgraph as csg

start_time = perf_counter()


def parse_input(p_in):
    cavern = []
    for row in p_in.splitlines():
        cavern.append([int(val) for val in row])
    return np.array(cavern)


def list_neighbours(coord, array_shape):
    neighbour_coords = set()
    neighbour_mask = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for x, y in neighbour_mask:
        new_coord = (x + coord[0], y + coord[1])
        if all([(coord > -1 and coord < array_shape[axis]) for axis, coord in enumerate(new_coord)]):
            neighbour_coords.add((new_coord))
    return neighbour_coords


def make_adj_matrix(cavern):
    coords = [tuple(coord) for coord in np.array(np.where(cavern)).T]
    adj_mat = pd.DataFrame(0,
                           columns=coords,
                           index=coords,
                           )
    for coord in coords:
        for neighbour in list_neighbours(coord, cavern.shape):
            adj_mat[coord][neighbour] = cavern[coord]
    return adj_mat


def calc_risk(p_in):
    cavern = parse_input(p_in)
    adj_mat = make_adj_matrix(cavern)
    path_costs = csg.shortest_path(adj_mat.to_numpy(), indices=[0])
    answer = int(path_costs[0, -1])
    print(f"\nAnswer: {answer}")


calc_risk(p_in)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
