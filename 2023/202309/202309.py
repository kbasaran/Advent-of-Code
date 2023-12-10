# 2023 Day 09

# ---- Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np

# ---- Part 1
start_time = perf_counter()

def parse_input(p_in):
    arrays = []
    for line in p_in.strip().splitlines():
        values = line.split()
        size = len(values)
        array = np.zeros((size, size), dtype=int)
        array[0,:] = values
        arrays.append(array)
    return arrays

arrays = parse_input(p_in)
for array in arrays:
    n_rows = array.shape[0]
    for i_row in range(1, n_rows):
        array[i_row, i_row:] = array[i_row - 1, i_row:] - array[i_row - 1, i_row-1:-1]       

next_values = [sum(arr[:, -1]) for arr in arrays]

print(f"Part 1:\n{sum(next_values)}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
start_time = perf_counter()

for i, array in enumerate(arrays):
    n_rows = array.shape[0]
    array = np.concatenate((np.zeros((n_rows, 1), dtype=int), array), axis=1)
    for i_row in reversed(range(n_rows-1)):
        array[i_row, i_row] = array[i_row, i_row+1] - array[i_row+1, i_row+1]
    arrays[i] = array

initial_values = [arr[0, 0] for arr in arrays]

print(f"Part 2:\n{sum(initial_values)}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
