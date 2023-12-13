# 2023 Day 12

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product, combinations
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


def count_possible_combinations_per_chunk(record_values, required_length):
    counter = 0
    for offset in range(len(record_values) - required_length + 1):
        outside_range = record_values[np.r_[0:offset, offset+required_length:len(record_values)]]
        if np.all(outside_range < 1):
            counter += 1
    return counter

# count_possible_combinations_per_chunk(np.array([0,0,1,0,0,0]), 3)

def possible_arrangements(record, amounts):
    
    record_as_list = list(record.replace("?", "0").replace(".", "1").replace("#", "2"))
    record_arr = np.array(record_as_list, dtype=int) - 1   # -1 is the question marks
    print(record_arr)
    print()
    split_indexes = dict()
    new_possible_split_indexes = list()
    for i in range(1, len(record_arr) - 1):
        char_prev, char = record_arr[[i-1, i]]

        # add existing split indexes
        # start index of groups of dots are split locations
        # e.g. ".", "..."
        if char == 0 and char_prev != 0:
                split_indexes[i] = set((i,))
                j = 1
                while i+j < len(record_arr) and record_arr[i + j] == 0:
                    # if i + j == len(record_arr) - 1:  # these "."'s connect to the end of the record
                        # split_indexes.pop(i)
                    # else:
                    split_indexes[i].add(i+j)
                    j += 1

        # if we need more split locations, which indexes may those be at
        elif np.all(record_arr[i-1:i+2] == -1):
                    new_possible_split_indexes.append(i)

    # create combinations with added split points
    # total amount of split points need to match the amount of lengths given by puzzle
    n_missing_split_points = len(amounts) - len(split_indexes)
    new_split_index_combinations = combinations(new_possible_split_indexes, n_missing_split_points)
    split_index_combinations = []
    for combo in new_split_index_combinations:
        # make a list of all split indexes, including the start (-1) and end (len)
        split_index_combo = sorted([-1, *split_indexes.keys(), *combo])
        if np.all(np.diff(split_index_combo) > 1):
            # sort out neighbouring split positions
            split_index_combinations.append(split_index_combo)


    # ---- Numpy

    chunks = np.zeros((len(split_index_combinations), len(record_arr) + 2), dtype=int)
    chunk_lengths = dict()

    for ic, split_combo in enumerate(split_index_combinations):

        combo_fail = False
        chunk_lengths[ic] = []
        score = 1

        print(split_combo)
        for iss, start_position in enumerate(split_combo[:-1]):
            # print(iss, start_position)
            # iss index location would be a "." the chunk start one index after it
            # print(type(split_indexes.get(start_position, [0])), split_indexes.get(start_position, [0]))
            start_index = max(start_position, max([-1, *split_indexes.get(start_position, [-1])])) + 1
            end_index = len(record_arr) if iss == len(split_combo) - 1 else split_combo[iss+1]
            if end_index - start_index < amounts[iss]:
                combo_fail = True
            if not combo_fail:
                chunks[ic, start_index:end_index] = 1
                chunk_lengths[ic].append((start_index, end_index))
                # print(start_index, end_index, record_arr[start_index:end_index])
                score *= count_possible_combinations_per_chunk(record_arr[start_index:end_index],
                                                               amounts[iss],
                                                               )

            else:
                chunks[ic, :] = -1

        print(score)
        # for each chunk, make a list of all possibilities, such as "110", "011"
        # then verify these against record_arr
        
        
        

    print(chunks)




    # ---- Python

    # for ic, split_combo in enumerate(split_index_combinations):

    #     # chunks = {key: [] for key in split_position}
    #     # values is possible positions for "#" elements
    #     # keys is start of a split point before the chunks
    #     chunks = list()
        
    #     for iss, start_position in enumerate(split_combo):
    #         # iss index location would be a "." the chunk start one index after it
    #         # print(type(split_indexes.get(start_position, [0])), split_indexes.get(start_position, [0]))
    #         start_index = max(start_position, max([-1, *split_indexes.get(start_position, [-1])])) + 1
    #         end_index = len(record_arr) if iss == len(split_combo) - 1 else split_combo[iss+1]
    #         chunks.append((start_index, end_index))

    #     print("\nfor split positions " + str(split_combo))
    #     print("chunk combination:")
    #     test_record = ["."] * len(record_arr)
    #     for chunk in chunks:
    #         for ic in range(chunk[0], chunk[1]):
    #             test_record[ic] = "#"
    #     print("".join(test_record))

    return split_index_combinations


arrangements = possible_arrangements("????.#..????..#...", (1, 2, 1, 1, 1))




# print(len(arrangements))
# print(arrangements)


# def trim_down_to_definite(record, amounts):    
#     record_new = record
#     new_amounts = amounts.copy()
#     while record_new[-1] == "?":
#         record_new = record_new.removesuffix("?")
#         new_amounts[-1] -= 1
#         if new_amounts


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
