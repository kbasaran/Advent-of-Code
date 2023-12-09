# 2023 Day 08

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from functools import lru_cache
import numpy as np

start_time = perf_counter()

# ---- Part 1

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MEMORY_DEPTH = 4

@lru_cache
def convert_loc_to_number(loc: str) -> int:
    assert len(loc) == 3
    base = len(letters)
    values = [base**i * letters.find(letter) for i, letter in enumerate(reversed(loc))]
    assert all([value >= 0 for value in values])
    return sum(values)

@lru_cache
def convert_number_to_loc(number: int) -> str:
    base = len(letters)
    orders = [-1] * 3
    orders[0], rest = divmod(number, base**2)
    orders[1], rest = divmod(rest, base**1)
    orders[2] = rest
    return letters[orders[0]] + letters[orders[1]] + letters[orders[2]]

def convert_dir_to_number(dir_in: str) -> int:
    return int(dir_in.replace("L", "1").replace("R", "2"), base=3)

def create_memory_array(p_in):
    global MEMORY_DEPTH
    base = len(letters)
    length = base**3
    memory = np.ndarray((length, 3**MEMORY_DEPTH), dtype=np.int16)
    memory[:, :] = -1
    print(f"Array size in memory: {memory.nbytes / 2**20:.2g}GB")
    return memory

def parse_input(p_in):
    array = create_memory_array(p_in)
    directions, connections = p_in.strip().split("\n\n")
    for line in connections.splitlines():
        loc, dirs = line.split(" = ")
        dir_left, dir_right = dirs.replace("(", "").replace(")", "").split(", ")
        array[convert_loc_to_number(loc), 1] = convert_loc_to_number(dir_left)
        array[convert_loc_to_number(loc), 2] = convert_loc_to_number(dir_right)
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

get_repeated_string("abc", 30, 33)

memory, directions = parse_input(p_in)

pos, loc = 0, 0
last_visited = [0]
while True:
    solution_found = False
    for instruction_length in reversed(range(1, MEMORY_DEPTH)):
        start_loc = loc
        instruction_chunk = get_repeated_string(directions, pos, pos+instruction_length)
        print(f"Attempting chunk {instruction_chunk}")
        instruction_as_number = convert_dir_to_number(instruction_chunk)
        loc_new = memory[loc, instruction_as_number]
        if loc_new == -1:
            continue
        else:
            # update to new position
            loc = loc_new
            pos += instruction_length
            print(f"Found in memory. Moving to: {convert_number_to_loc(loc_new)}\n")

            if loc == len(letters)**3 - 1:
                solution_found = True

            # instruction that we used to reach here. can not be longer than memory_depth
            stored_steps_length = len(last_visited)
            stored_steps_instruction = get_repeated_string(directions, pos-stored_steps_length, pos)
            stored_steps_instruction_as_number = convert_dir_to_number(stored_steps_instruction)
            
            # update what we know
            filler = [-1] * instruction_length
            last_visited.append(filler)  # jump steps as long as the instruction length
            last_visited[-1] = loc  # add this new location
            last_visited = last_visited[-MEMORY_DEPTH:]  # trim
            memory[last_visited[0], stored_steps_instruction_as_number] = loc
    if solution_found:
        print(f"Finito! Position: {pos}")
        break


print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
