# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:37:58 2020

@author: kerem.basaran
"""

import pandas as pd
import numpy as np

with open("input.txt") as f:
    p_in = [int(i) for i in f.read().splitlines()]

# %% Part 1
joltages = [0] + p_in + [max(p_in) + 3]

jl = pd.Series(joltages, name="joltage").astype(int).sort_values(ignore_index=True)
jldiffs = (jl - jl.shift(1)).dropna()

print(jldiffs.value_counts())
print()

# %% Part 2
# jl = jl.values
portions = []
i, portion = 0, []
while i < len(jl):
    val = jl[i]
    if len(portion) == 0:
        portion.append(val)
        i += 1
    elif (val - 3 == portion[-1]) & (len(portion) > 1):
        portions.append(portion)
        portion = [val]
        i += 1
    else:
        portion.append(val)
        i += 1


def find_paths(portion, pos=0):
    paths = [0, 0, 0, 0]
    step = 1
    while (step <= 3) & ((pos + step) < len(portion)):
        next_3_vals = [portion[pos] + 1, portion[pos] + 2, portion[pos] + 3]
        if portion[pos+step] in next_3_vals:
            sub_paths = find_paths(portion[pos:], step)
            paths[step] = (sub_paths if sub_paths > 1 else 1)
        step += 1

    return sum(paths)


n_path = np.array([], dtype=np.int64)
for portion in portions:
    n_path = np.append(n_path, find_paths(portion))
print(f"Number of separate paths: {np.product(n_path)}")

