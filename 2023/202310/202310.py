# 2023 Day 10

# ---- Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
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
    
    costs = sparse.dok_array((n_rows*n_cols, n_rows*n_cols), dtype=int)
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

print(f"Part 1:\n{max([int(dist) for dist in paths if dist != np.inf])}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
