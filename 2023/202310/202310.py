# 2023 Day 10

# ---- Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import scipy.sparse as sparse
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 300

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
    return sketch, costs, start_pos

sketch, costs, start_pos = parse_input(p_in)
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
        path1.append(int(pos))

    pos = furthest_pos
    path2 = []
    while pos != start_pos:
        pos = predecessors2[pos]
        path2.append(int(pos))
            
    # return reversed([*reversed(path1[:-1]), furthest_pos, *path2])  # first element is S start
    return [*reversed(path2), furthest_pos, *path1[:-1]]  # first element is S start


def convert_flat_pos_to_tuple_coord(n_cols, flat_pos):
    return divmod(flat_pos, n_cols)

def convert_tuple_coord_to_flat_pos(n_cols, i, j):
    return i * n_cols + j

def directed_neighbours(sketch, i, j, directions):
    neighbours = set()
    if "e" in directions:
        neighbours.add((i, j+1))
    if "w" in directions:
        neighbours.add((i, j-1))
    if "n" in directions:
        neighbours.add((i-1, j))
    if "s" in directions:
        neighbours.add((i+1, j))
    
    return [coord for coord in neighbours if validate_coordinates(sketch, *coord)]

def validate_coordinates(sketch, i, j):
    n_cols = len(sketch[0])
    n_rows = len(sketch)
    if i >= n_rows or i < 0 or j >= n_cols or j < 0:
        return False
    else:
        return True

def get_inside_neighbours_to_path(loop_elements, sketch):
    resolved = set()
    left_neighbours = set()
    right_neighbours = set()
    n_cols = len(sketch[0])
    n_rows = len(sketch)
    len_loop = len(loop_elements)
    
    index = 1  # first element was the start element
        
    while len(resolved) != len_loop:
        pos_pre = loop_elements[(index-1) % len_loop]
        pos = loop_elements[(index) % len_loop]
        i_pre, j_pre = convert_flat_pos_to_tuple_coord(n_cols, pos_pre)
        i, j = convert_flat_pos_to_tuple_coord(n_cols, pos)
        letter = sketch[i][j]

        neigh = {"n": (i-1, j),
                 "s": (i+1, j),
                 "w": (i, j-1),
                 "e": (i, j+1),
                 "nw": (i-1, j-1),
                 "sw": (i+1, j-1),
                 "ne": (i-1, j+1),
                 "se": (i+1, j+1),
                 }
        
        for key, val in neigh.items():
            ni, nj = val
            if not validate_coordinates(sketch, ni, nj):
                neigh[key] = None

        # eastwards
        if j == j_pre + 1:
            # all on the sides (some coincide with self but those will be removed later)
            left_neighbours.add(neigh["n"])
            right_neighbours.add(neigh["s"])
            # turning north
            if letter == "J":
                left_neighbours.add(neigh["nw"])
                right_neighbours.add(neigh["se"])
                
                right_neighbours.add(neigh["e"])
            # turning south
            elif letter == "7":
                left_neighbours.add(neigh["e"])
                
                left_neighbours.add(neigh["ne"])
                right_neighbours.add(neigh["sw"])

        # northwards
        elif i == i_pre - 1:
            left_neighbours.add(neigh["w"])
            right_neighbours.add(neigh["e"])
            # turning west
            if letter == "7":
                left_neighbours.add(neigh["sw"])
                right_neighbours.add(neigh["ne"])
                
                right_neighbours.add(neigh["n"])
            # turning east
            elif letter == "F":
                left_neighbours.add(neigh["n"])
                
                left_neighbours.add(neigh["nw"])
                right_neighbours.add(neigh["se"])

        # westwards
        elif j == j_pre - 1:
            left_neighbours.add(neigh["s"])
            right_neighbours.add(neigh["n"])
            # turning south
            if letter == "F":
                left_neighbours.add(neigh["se"])
                right_neighbours.add(neigh["nw"])
                
                right_neighbours.add(neigh["w"])
            # turning north
            elif letter == "L":
                left_neighbours.add(neigh["w"])
                
                left_neighbours.add(neigh["sw"])
                right_neighbours.add(neigh["ne"])

        # southwards
        elif i == i_pre + 1:
            left_neighbours.add(neigh["e"])
            right_neighbours.add(neigh["w"])
            # turning east
            if letter == "L":
                left_neighbours.add(neigh["ne"])
                right_neighbours.add(neigh["sw"])
                
                right_neighbours.add(neigh["s"])
            # turning west
            elif letter == "J":
                left_neighbours.add(neigh["s"])
                
                left_neighbours.add(neigh["se"])
                right_neighbours.add(neigh["nw"])

        resolved.add(pos)
        index = (index+1) % len_loop

    # remove the None values
    left_neighbours = [convert_tuple_coord_to_flat_pos(n_cols, *els) for els in left_neighbours if els]
    right_neighbours = [convert_tuple_coord_to_flat_pos(n_cols, *els) for els in right_neighbours if els] 
    
    # pick one as inner
    inner = left_neighbours if len(left_neighbours) < len(right_neighbours) else right_neighbours
    
    # return all that is not in loop_elements
    return [pos for pos in inner if pos not in loop_elements]


def show_image_from_pos(sketch, loop_elements, inner):
    n_cols = len(sketch[0])
    n_rows = len(sketch)
    array = np.zeros((n_rows, n_cols), dtype=int)

    for point in inner:
        if isinstance(point, tuple):
            i, j = point
        elif isinstance(point, int):
            i, j = convert_flat_pos_to_tuple_coord(n_cols, point)
        else:
            # pass
            raise ValueError
        array[i, j] = 16

    for point in loop_elements:
        if isinstance(point, tuple):
            i, j = point
        elif isinstance(point, int):
            i, j = convert_flat_pos_to_tuple_coord(n_cols, point)
        else:
            raise ValueError
        array[i, j] = 8

    plt.imshow(array)


def grow_direct_neighbours(sketch, inner_neighbours, loop_elements):
    n_cols = len(sketch[0])
    elements = set(inner_neighbours)
    while True:
        new_neighbours = set()
        for flat_pos in elements:
            i, j = convert_flat_pos_to_tuple_coord(n_cols, flat_pos)
            directed_ns = directed_neighbours(sketch, i, j, "ewns")
            for neighbour in directed_ns:
                directed_neighbour_pos = convert_tuple_coord_to_flat_pos(n_cols, *neighbour)
                if directed_neighbour_pos not in loop_elements and directed_neighbour_pos not in elements:
                    new_neighbours.add(directed_neighbour_pos)
        if not new_neighbours:
            return elements
        else:
            elements = elements.union(new_neighbours)


loop_elements = get_elements_of_loop(costs, start_pos, furthest_pos)
inner_neighbours = get_inside_neighbours_to_path(loop_elements, sketch)
inner_circled = grow_direct_neighbours(sketch, inner_neighbours, loop_elements)

show_image_from_pos(sketch, loop_elements, inner_neighbours)
show_image_from_pos(sketch, loop_elements, inner_circled)

print(f"Part 2: {len(inner_circled)}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
