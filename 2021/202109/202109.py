# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np

start_time = perf_counter()


def parse_input(p_in):
    global floor
    rows = []
    for row in p_in.split("\n"):
        rows.append([int(val) for val in row])
    floor = np.array(rows, dtype=int)

    

parse_input(p_in)


def find_neigbour_coords(floor, coord):
    neighbour_coords = set()
    for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_coord = (x + coord[0], y + coord[1])
        if new_coord in list_of_coords(floor):
            neighbour_coords.add((new_coord))
    return neighbour_coords


def list_of_coords(floor):
    return set(np.ndindex(floor.shape))


def part_1(floor):
    low_points = {}  # key is coordinates, value is risk level
    for coord in list_of_coords(floor):
        value = floor[coord]
        neigh_vals = [floor[neigh_coord] for neigh_coord in find_neigbour_coords(floor, coord)]
        if all([value < neigh_val for neigh_val in neigh_vals]):
            low_points[coord] = value + 1
    sum_risk_levels = sum(low_points.values())
    print(f"\n--Part 1--\nAnswer: {sum_risk_levels}")


part_1(floor)


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
