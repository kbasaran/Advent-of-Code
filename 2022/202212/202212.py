# 2022 Day 12

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import scipy.sparse as sparse


start_time = perf_counter()


def parse_input(p_in):
    cavern = []
    for row in p_in.splitlines():
        cavern.append([ord(val) for val in row])
    array = np.array(cavern, dtype=np.int32)
    start_coord = tuple([ans[0] for ans in np.where(array == 83)])
    end_coord = tuple([ans[0] for ans in np.where(array == 69)])
    array[start_coord] = ord("a")
    array[end_coord] = ord("z")
    return array, start_coord, end_coord


def list_neighbours(coord, array_shape):
    neighbour_coords = set()
    neighbour_mask = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for x, y in neighbour_mask:
        new_coord = (x + coord[0], y + coord[1])
        if all([(coord > -1 and coord < array_shape[axis]) for axis, coord in enumerate(new_coord)]):
            neighbour_coords.add((new_coord))
    return neighbour_coords

def flat_coord(coord, array_shape):
    return coord[0] * array_shape[1] + coord[1]

def path_step_costs(cavern):
    coords = [tuple(coord) for coord in np.array(np.where(cavern)).T]
    step_costs = sparse.dok_array((cavern.size, cavern.size), dtype=np.int32)
    for coord in coords:
        for neighbour in list_neighbours(coord, cavern.shape):
            step_cost = cavern[neighbour] - cavern[coord]
            if step_cost <= 1:
                step_costs[flat_coord(coord, cavern.shape), flat_coord(neighbour, cavern.shape)] = 1
    return step_costs


if __name__ == "__main__":
    cavern, i_start, i_end = parse_input(p_in)
    step_costs = path_step_costs(cavern)
    path_costs = sparse.csgraph.shortest_path(step_costs, indices=flat_coord(i_start, cavern.shape))
    print(path_costs[flat_coord(i_end, cavern.shape)])

    possible_starts = np.flatnonzero(cavern == 97)
    path_costs_part2 = [costs[flat_coord(i_end, cavern.shape)] for costs in sparse.csgraph.shortest_path(step_costs, indices=possible_starts)]
    print(min(path_costs_part2))


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
