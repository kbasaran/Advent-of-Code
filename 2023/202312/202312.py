# 2023 Day 12

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product, combinations
import numpy as np
from math import comb
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
start_time = perf_counter()


def count_possible_combinations_per_chunk(record_values, required_length):
    counter = 0
    for offset in range(len(record_values) - required_length + 1):
        outside_range = record_values[np.r_[0:offset, offset+required_length:len(record_values)]]
        if np.all(outside_range < 1):
            counter += 1
    return counter

# count_possible_combinations_per_chunk(np.array([0,0,1,0,0,0]), 3)

def make_record_into_array(record):
    record_as_list = list(record.replace("?", "0").replace(".", "1").replace("#", "2"))
    # record_arr = np.zeros(len(record_as_list) + 2, dtype=int)
    record_arr = [int(val) - 1 for val in record_as_list]
    # -1 is the question marks
    return record_arr


def possible_arrangements(record_arr, amounts):

    # print()
    # print("--------", record_arr, amounts)
    split_indexes = [[-1]]
    chunks = list()
    for i, val in enumerate(record_arr):
        val_prev = 0 if i == 0 else record_arr[i-1]

        # add existing split indexes
        # start index of groups of dots are split locations
        # e.g. ".", "..."
        if val == 0 and val_prev != 0:
            split_indexes.append([i])
            j = 1
            while i+j < len(record_arr) and record_arr[i + j] == 0:
                split_indexes[-1].append(i+j)
                j += 1
        elif val == 1 or val == -1:
            if val_prev == 0:
                chunks.append([i, i + 1])
            else:
                chunks[-1][-1] = i + 1

    # print(f"existing split positions: {split_indexes}")
    # print(f"chunks: {chunks}")

    # # create combinations with added split points
    # total amount of split points need to match the amount of lengths given by puzzle
    n_missing_split_points = len(amounts) - len(chunks)
    # print(f"missing split points: {n_missing_split_points}")

    # in which chunks to add these new splits into
    addition_combos = np.ones(((n_missing_split_points + 1)**len(chunks), len(chunks)), dtype=int)
    for i, combo in enumerate(product(range(n_missing_split_points + 1), repeat=len(chunks))):
        addition_combos[i, :] += combo
    # print(f"new amounts to split into per tag: {addition_combos[np.sum(addition_combos, axis=1) == len(amounts)]}")

    scores = []
    for row in addition_combos[np.sum(addition_combos, axis=1) == len(amounts)]:
        # print("------combination:", row)
        scores_per_chunk = []
        for i_section, n_chunks in enumerate(row):
            # print("----section", i_section, n_chunks, "piece")
            start_index = chunks[i_section][0]
            end_index = chunks[i_section][1]
            record_chunk = np.array(record_arr[start_index:end_index])
            amounts_start_index = np.sum(row[:i_section])
            expected_amount = amounts[amounts_start_index:amounts_start_index+n_chunks]
            free_play = len(record_chunk) - sum(expected_amount) - len(expected_amount) + 1
            # print("record and amount:", record_chunk, expected_amount)
            
            offset_scores = []
            # print("--offsets")
            for offset in range(free_play + 1):
                # print("offset", offset)
                len_1 = expected_amount[0]
                if (offset == 0 or np.all(record_chunk[:offset] != 1)) and (offset+len_1 == len(record_chunk) or record_chunk[offset+len_1] != 1):
                    score_offset = 1
                else:
                    score_offset = 0
                    continue
                if len(expected_amount) > 1:
                    score_offset *= possible_arrangements(record_chunk[expected_amount[0] + 1 + offset:], expected_amount[1:])
                offset_scores.append(score_offset)
                # print("offset scores: ", offset_scores)

            scores_per_chunk.append(sum(offset_scores))
        # print("chunk scores:", scores_per_chunk)
        scores.append(np.prod(scores_per_chunk))
    # print("scores per combination:", scores)
        

    return(np.sum(scores))



# arrangements = possible_arrangements("???.###", (1,1,3))
# arrangements = possible_arrangements(".??..??...?##.", (1,1,3))
# arrangements = possible_arrangements("?#?#?#?#?#?#?#?", (1,3,1,6))
# arrangements = possible_arrangements("????.#...#...", (4,1,1))
# arrangements = possible_arrangements("????.######..#####.", (1,6,5))
# arrangements = possible_arrangements("?###????????", (3, 2, 1))  # 10




arrangements_per_line = []
for i, (record, amounts) in enumerate(record_lines):
    record_arr = make_record_into_array(record)
    arrangements_per_line.append(possible_arrangements(record_arr, amounts))
    print()
    print(f"Solved row {i}: '{record}' {arrangements_per_line[-1]} combinations")
    print(f"Elapsed time: {(perf_counter() - start_time) * 1000:.3g} ms")


print(f"Part 2:\n{sum(arrangements_per_line)}")


# print(f"Part 2:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
# print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
