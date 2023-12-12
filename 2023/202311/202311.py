# 2023 Day 11

# ---- Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
from itertools import product

# ---- Part 1
start_time = perf_counter()

def parse_input(p_in):
    n_cols = len(p_in.strip().partition("\n")[0])
    n_rows = len(p_in.strip().splitlines())

    p_in = p_in.strip().replace(".", "0").replace("#", "1")
    sketch = np.zeros((n_rows, n_cols), dtype=int)
    for i, line in enumerate(p_in.strip().splitlines()):
        sketch[i, :] = [int(val) for val in line]
    
    stars = [(i, j) for i, j in zip(*np.where(sketch == 1))]

    return sketch, stars

def get_expanding(sketch):
    rows = np.where(~sketch.any(axis=1))[0]
    cols = np.where(~sketch.any(axis=0))[0]

    return rows, cols

def get_pairs(stars):
    pairs = set()
    couples = product(stars, repeat=2)
    for a, b in couples:
        if a != b:
            pairs.add(frozenset([frozenset([a]), frozenset([b])]))
    return pairs

def calc_distances(pairs, expanding_rows, expanding_cols, expanded_size=1):
    distances = {}
    for pair in pairs:
        p1, p2 = tuple(pair)
        i1, j1 = tuple(p1)[0]
        i2, j2 = tuple(p2)[0]
        distance_direct = abs(i1 - i2) + abs(j1 - j2)
        extra_rows = expanding_rows[(expanding_rows < max(i1, i2)) & (expanding_rows > min(i1, i2))]
        extra_cols = expanding_cols[(expanding_cols < max(j1, j2)) & (expanding_cols > min(j1, j2))]
        distances[pair] = distance_direct + (len(extra_rows) + len(extra_cols)) * (expanded_size - 1)
        # print(pair, distance_direct, extra_rows, extra_cols)
    return distances


sketch, stars = parse_input(p_in)
expanding_rows, expanding_cols = get_expanding(sketch)
pairs = get_pairs(stars)
distances = calc_distances(pairs, expanding_rows, expanding_cols, expanded_size=1)

print(f"Part 1:\n{sum(distances.values())}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
start_time = perf_counter()

distances = calc_distances(pairs, expanding_rows, expanding_cols, expanded_size=1_000_000)

print(f"Part 2:\n{sum(distances.values())}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
