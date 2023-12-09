# 2023 Day 08

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
import pandas as pd

start_time = perf_counter()

# ---- Part 1

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def convert_dir_to_number(dir_in: str) -> int:
    return int(dir_in.replace("L", "1").replace("R", "2"), base=3)

def create_memory_array():
    column_names = ["".join(letters) for letters in product(letters, repeat=3)]
    memory = pd.DataFrame(columns=column_names, index=[1,2])
    return memory

def parse_input(p_in):
    array = create_memory_array()
    directions, connections = p_in.strip().split("\n\n")
    for line in connections.splitlines():
        loc, dirs = line.split(" = ")
        dir_left, dir_right = dirs.replace("(", "").replace(")", "").split(", ")
        array.at[1, loc] = dir_left
        array.at[2, loc] = dir_right
    return array, directions

def get_repeated_string(seed_string, start, end):
    if start > end:
        raise ValueError("Invalid range: start should be less than or equal to end")
    len_seed = len(seed_string)
    reduce = start // len_seed
    start -= len_seed * reduce
    end -= len_seed * reduce
    periods = end // len_seed + 1
    raw = seed_string * periods

    return raw[start:end]

memory, directions = parse_input(p_in)
pos, loc = 0, "AAA"
while loc != "ZZZ":
    instruction = get_repeated_string(directions, pos, pos+1)
    # print(f"Handling instruction {instruction}")
    instruction_as_number = convert_dir_to_number(instruction)
    loc = memory.at[instruction_as_number, loc]
    pos += 1

print(f"Part 1: {pos}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
