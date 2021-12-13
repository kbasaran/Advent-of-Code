# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
from scipy import sparse
from collections import namedtuple

start_time = perf_counter()


def parse_input(p_in):
    global floor
    rows = []
    for row in p_in.split("\n"):
        rows.append([int(val) for val in row])
    floor = np.array(rows, dtype=int)


parse_input(p_in)


def find_neigbour_coords(coord, floor_shape) -> set:
    neighbour_coords = set()
    for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_coord = (x + coord[0], y + coord[1])
        if all([(coord > -1 and coord < floor_shape[axis]) for axis, coord in enumerate(new_coord)]):
            neighbour_coords.add((new_coord))
    return neighbour_coords


def list_of_coords(floor):
    return set(np.ndindex(floor.shape))


def part_1(floor):
    low_points = {}  # key is coordinates, value is risk level
    for coord in list_of_coords(floor):
        value = floor[coord]
        neigh_vals = [floor[neigh_coord] for neigh_coord in find_neigbour_coords(coord, floor.shape)]
        if all([value < neigh_val for neigh_val in neigh_vals]):
            low_points[coord] = value + 1
    sum_risk_levels = sum(low_points.values())
    print(f"\n--Part 1--\nAnswer: {sum_risk_levels}")


part_1(floor)

print("\n--Part 2--")

floor = 9 - floor
floor_sparse = sparse.dok_matrix(floor)

basins = []  # key is first item found, values are the coordinates in it
keys_without_home = set([key for key in floor_sparse.keys() if floor_sparse[key] > 0])
keys_to_solve = len(keys_without_home)
counter = 0
mid_time = perf_counter()

while len(keys_without_home) > 0:
    len_key_without_home = len(keys_without_home)
    for basin in basins:
        while True:
            found_keys_this_basin = set()
            for i, key in enumerate(keys_without_home):
                neighbours_of_this_coord = find_neigbour_coords(key, floor.shape)
                if any([basin_coord in neighbours_of_this_coord for basin_coord in basin["coords"]]):
                    basin["coords"].add(key)
                    found_keys_this_basin.add(key)
                    counter += 1
            for key in found_keys_this_basin:
                keys_without_home.remove(key)
            if len(keys_without_home) - 1 == i or len(keys_without_home) == 0:
                break
    if len_key_without_home == len(keys_without_home):
        # make a new basin
        key = keys_without_home.pop()
        new_basin = {"name": key,
                     "coords": set([key]),
                     }
        basins.append(new_basin)

    if counter > 199:
        print(f"\nKeys left: {len(keys_without_home)}")
        print(f"Basin count: {len(basins)}")
        print(f"Expected time left: {len(keys_without_home) * (perf_counter() - start_time) / (keys_to_solve - len(keys_without_home)) / 60:.1f} minutes")
        counter = 0

basin_sizes = [len(basin["coords"]) for basin in basins]
prod_max_3 = np.product(sorted(basin_sizes)[-3:])
print(f"\nAnswer: {prod_max_3}")

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")

import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 150
plt.title("202109 Ocean floor\n(dark is deep)")
plt.imshow(floor)