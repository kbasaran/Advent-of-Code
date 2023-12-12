# 2023 Day 12

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
import numpy as np
# from functools import lru_cache

# ---- Part 1
start_time = perf_counter()

def parse_input(p_in):
    record_lines = []
    for line in p_in.strip().splitlines():
        record, amounts_str = line.split()
        record_lines.append((record, [int(val) for val in amounts_str.split(",")]))
    
    return record_lines  # tuple of record and amount

# @lru_cache
def make_arrangement(length, amounts, shift):
    arr = np.zeros(length, dtype=int)
    for i, (amount, shift_1) in enumerate(zip(amounts, shift)):
        start = i + sum(amounts[:i]) + shift_1
        end = start + amount
        arr[start:end] = 1
    return arr

def possible_arrangements(record, amounts):
    len_t = len(record)
    play_range = len_t - sum(amounts) - len(amounts) + 2

    shifts = product(range(play_range), repeat=len(amounts))
    # print(f"Started filtering of {2**play_range} possible arrangements.")
    shifts = [shift for shift in shifts if tuple(sorted(shift)) == shift]

    record_as_list = list(record.replace("?", "0").replace(".", "1").replace("#", "2"))
    record_arr = np.array(record_as_list, dtype=int) - 1   # -1 is the question marks
    known_indexes = np.where(record_arr != -1)

    arrangements = list()
    for shift in shifts:
        test_arr = make_arrangement(len_t, amounts, shift)
        if all(test_arr[known_indexes] == record_arr[known_indexes]):
            arrangements.append(test_arr)
    
    return arrangements

record_lines = parse_input(p_in)
arrangements_per_line = []
for record, amounts in record_lines:
    arrangements_per_line.append(possible_arrangements(record, amounts))

print(f"Part 1:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
# start_time = perf_counter()

# def modify_input_for_part_2(record_lines, n_fold=5):
#     record_lines_long = []
#     for record, amounts in record_lines:
#         record_long = record * n_fold
#         amounts_long = amounts * n_fold
#         record_lines_long.append((record_long, amounts_long))
#     return record_lines_long

# record_lines_long = modify_input_for_part_2(record_lines, n_fold=5)
# arrangements_per_line = []
# for i, (record, amounts) in enumerate(record_lines_long):
#     print(f"Solving line {i}:\n{record}, {amounts}")
#     arrangements = possible_arrangements(record, amounts)
#     print(f"Number of arrangements possible: {len(arrangements)}")
#     arrangements_per_line.append(arrangements)
#     print(f"Elapsed time: {(perf_counter() - start_time) / 60:.3g} min.\n")


# print(f"Part 2:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
# print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
