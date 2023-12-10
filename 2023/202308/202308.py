# 2023 Day 08

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
import pandas as pd
import math

# ---- Part 1
start_time = perf_counter()

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_memory_array(repeat):
    column_names = ["".join(letters) for letters in product(letters, repeat=repeat)]
    memory = pd.DataFrame(columns=column_names, index=["L", "R"], dtype=str).fillna(0)
    return memory

def parse_input(p_in):
    array = create_memory_array(3)
    directions, connections = p_in.strip().split("\n\n")
    for line in connections.splitlines():
        loc, dirs = line.split(" = ")
        dir_left, dir_right = dirs.replace("(", "").replace(")", "").split(", ")
        array.at["L", loc] = dir_left
        array.at["R", loc] = dir_right
    return array, directions

def get_pos_from_repeated_string(seed_string, pos):
    len_seed = len(seed_string)
    reduce = pos // len_seed
    pos -= len_seed * reduce
    return seed_string[pos]

memory, directions = parse_input(p_in)
pos, loc = 0, "AAA"
while loc != "ZZZ":
    instruction = get_pos_from_repeated_string(directions, pos)
    # print(f"Handling instruction {instruction}")
    loc = memory.at[instruction, loc]
    pos += 1

print(f"Part 1: {pos}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
start_time = perf_counter()

start_locations = memory.loc[:, memory.columns.str.endswith("A") & (memory != 0).any(axis=0)].columns
states = {start_location: (0, start_location) for start_location in start_locations}
pos = 0
while any([loc[2] != "Z" for _, loc in states.values()]):
    instruction = get_pos_from_repeated_string(directions, pos)
    for start_location, (_, loc) in states.items():
        if loc[2] != "Z":
            states[start_location] = (pos + 1, memory.at[instruction, loc])
    pos += 1

print(f"Part 2:\n{states}\nLCM: {math.lcm(*[val[0] for val in states.values()])}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.")
