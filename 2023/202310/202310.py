# 2023 Day 10

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import scipy.sparse as sparse
import numpy as np

# ---- Part 1
start_time = perf_counter()

def parse_input(p_in):
    sketch = []
    for line in p_in.strip().splitlines():
        elements = list(line)
        sketch.append(elements)
    n_cols = len(p_in.strip().partition("\n")[0])
    n_rows = len(p_in.strip().splitlines())
    n_elements = n_cols * n_rows
    
    costs = sparse.dok_array((n_elements, n_elements), dtype=int)
    for i in range(n_rows):
        for j in range(n_cols):
            val = sketch[i][j]
            flat_pos = i * n_cols + j
            # east
            if val in "FL-S" and j != n_cols-1 and sketch[i][j+1] in "J7-S":
                costs[flat_pos, flat_pos+1] = 1
            # west
            if val in "J7-S" and j != 0 and sketch[i][j-1] in "FL-S":
                costs[flat_pos, flat_pos-1] = 1
            # north
            if val in "LJ|S" and i != 0 and sketch[i-1][j] in "F7|S":
                costs[flat_pos, flat_pos-n_cols] = 1
            # south
            if val in "F7|S" and i != n_rows-1 and sketch[i+1][j] in "LJ|S":
                costs[flat_pos, flat_pos+n_cols] = 1
            if val == "S":
                start_pos = flat_pos

    # print(costs)
    return costs, start_pos

costs, start_pos = parse_input(p_in)
paths = sparse.csgraph.shortest_path(costs, indices=start_pos)
furthest_pos = max([int(dist) for dist in paths if dist != np.inf])

print(f"Part 1:\n{furthest_pos}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
def get_elements_of_loop(costs, start_pos, furthest_pos):
    dir1_next, dir2_next = [key[1] for key in costs[[furthest_pos], :].keys()]

    # Path for direction 1
    costs_dir1 = costs.copy()
    costs_dir1[furthest_pos, dir1_next] = 0
    costs_dir1[dir1_next, furthest_pos] = 0
    _, predecessors1 = sparse.csgraph.shortest_path(costs_dir1, indices=start_pos, return_predecessors=True)
    
    # Path for direction 2
    costs_dir2 = costs.copy()
    costs_dir2[furthest_pos, dir2_next] = 0
    costs_dir2[dir2_next, furthest_pos] = 0
    _, predecessors2 = sparse.csgraph.shortest_path(costs_dir2, indices=start_pos, return_predecessors=True)

    pos = furthest_pos
    path1 = []
    while pos != start_pos:
        pos = predecessors1[pos]
        path1.append(pos)

    pos = furthest_pos
    path2 = []
    while pos != start_pos:
        pos = predecessors2[pos]
        path2.append(pos)
            
    return [*reversed(path1[:-1]), furthest_pos, *path2]


def costs_table_with_path_as_barrier(p_in, loop_elements):
    n_cols = len(p_in.strip().partition("\n")[0])
    n_rows = len(p_in.strip().splitlines())
    n_elements = n_cols * n_rows
    costs = sparse.dok_array((n_elements+1, n_elements+1), dtype=int)  # +1 for "external"
    external_element = n_elements
    for i in range(n_rows):
        for j in range(n_cols):
            flat_pos = i * n_cols + j
            if flat_pos not in loop_elements:
                neighbours = set()
                # not east border
                if j != n_cols - 1:
                    neighbours.add(flat_pos + 1)
                # not west border
                if j != 0:
                    neighbours.add(flat_pos - 1)
                # not north border
                if i != 0:
                    neighbours.add(flat_pos - n_cols)
                # not south border
                if i != n_rows - 1:
                    neighbours.add(flat_pos + n_cols)

                for neighbour in neighbours:
                    if neighbour not in loop_elements:
                        costs[flat_pos, neighbour] = 1
    
                # if on the border connect to "external"
                if i == 0 or (i == n_rows - 1) or j == 0 or (j == n_cols - 1):
                    costs[flat_pos, external_element] = 2
                    costs[external_element, flat_pos] = 2


    return costs, external_element

loop_elements = get_elements_of_loop(costs, start_pos, furthest_pos)
costs, external_element = costs_table_with_path_as_barrier(p_in, loop_elements)
paths = sparse.csgraph.shortest_path(costs, indices=external_element, directed=False)

unaccessible_coordinates = set()
for i in range(len(paths)):
    if paths[i] == np.inf and i not in loop_elements:
        unaccessible_coordinates.add(i)

print(sorted(unaccessible_coordinates))

print(f"Part 2:\n{len(unaccessible_coordinates)}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")