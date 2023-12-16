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
# start_time = perf_counter()


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

    print()
    print("------", record_arr, amounts)
    split_indexes = [-1]
    chunks = list()
    new_possible_split_indexes = list()
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

            # if we need more split locations, which indexes may those be at
            if np.all((record_arr[i-1:i+1] != 0) * (record_arr[i] == -1)):
                new_possible_split_indexes.append(i)

    print(f"existing split positions: {split_indexes}")
    print(f"chunks: {chunks}")

    # print(f"new possible split positions: {new_possible_split_indexes}")

    # # create combinations with added split points
    # total amount of split points need to match the amount of lengths given by puzzle
    n_missing_split_points = len(amounts) - len(chunks)
    print(f"missing split points: {n_missing_split_points}")
    # if n_missing_split_points < 1:  # why was it negative in some case??
    #     split_index_combinations = [[*split_indexes.keys()],]
    # else:
    #     new_split_index_combinations = combinations(new_possible_split_indexes, n_missing_split_points)
    #     split_index_combinations = []
    #     for combo in new_split_index_combinations:
    #         # make a list of all split indexes, including the start (-1) and end (len)
    #         split_index_combo = sorted([*split_indexes.keys(), *combo])
    #         if np.all(np.diff(split_index_combo) > 1):
    #             # sort out neighbouring split positions
    #             split_index_combinations.append(split_index_combo)
    # print(f"Combined split positions: {split_index_combinations}")

    # in which chunks to add these new splits into
    addition_combos = np.ones(((n_missing_split_points + 1)**len(chunks), len(chunks)), dtype=int)
    # addition_combos[:, :] = range(len(chunks))
    for i, combo in enumerate(product(range(n_missing_split_points + 1), repeat=len(chunks))):
        addition_combos[i, :] += combo
    print(f"new amounts to split into per tag: {addition_combos[np.sum(addition_combos, axis=1) == len(amounts)]}")

    scores = []
    for row in addition_combos[np.sum(addition_combos, axis=1) == len(amounts)]:
        print("----combination:", row)
        scores_per_chunk = []
        for i_section, n_chunks in enumerate(row):
            print("--section", i_section, n_chunks, "piece")
            start_index = chunks[i_section][0]
            end_index = chunks[i_section][1]
            record_chunk = np.array(record_arr[start_index:end_index])
            amounts_start_index = np.sum(row[:i_section])
            expected_amount = amounts[amounts_start_index:amounts_start_index+n_chunks]
            print("record and amount:", record_chunk, expected_amount)

            if n_chunks == 1 and len(record_chunk) == expected_amount[0]:
                score = 1

            elif n_chunks > 1 and np.any(record_chunk[1:-1] == -1):
                break_size = len(record_chunk) - sum(expected_amount)
                break_points = np.where(record_chunk[1:-1] == -1)[0] + 1
                version_score = []
                for break_point in break_points:
                    print("breaking at index", break_point)
                    score_first_part = count_possible_combinations_per_chunk(record_chunk[:break_point], expected_amount[0])
                    score_second_part = possible_arrangements(record_chunk[break_point+break_size:], expected_amount[1:])
                    version_score.append(score_first_part * score_second_part)
                score = sum(version_score)

            else:
                score = 0
            print("chunk score:", score)
            scores_per_chunk.append(score)
        scores.append(np.prod(scores_per_chunk))
    print("scores per combination:", scores)
        

    return(np.sum(scores))







    # ---- Numpy

    # chunks = np.zeros((len(split_indexes), len(record_arr) + 2), dtype=int)
    # chunk_lengths = dict()

    # split_combo = []
    # # score = 1

    # for iss, start_position in enumerate([*split_combo[:-1]]):
    #     print(iss, "start_position:", start_position)
    #     # iss index location would be a "." the chunk start one index after it
    #     print(type(split_indexes.get(start_position, [0])), split_indexes.get(start_position, [0]))
    #     start_index = max(
    #         start_position,
    #         max([-1, *split_indexes.get(start_position, [-1])]),
    #                     ) + 1
    #     end_index = len(record_arr) if iss == len(split_combo) else split_combo[iss+1]
    #     print(start_index, end_index, record_arr[start_index:end_index], amounts[iss])

    #     possibilities = end_index - start_index - amounts[iss] + 1
    #     if possibilities == 0:
    #         # combo_fail = True
    #         print("score:", 0)
    #     else:
    #         score = possibilities
    #         # chunks[ic, start_index:end_index] = 1
    #         # chunk_lengths[ic].append((start_index, end_index))
    #         # score_of_chunk = count_possible_combinations_per_chunk(record_arr[start_index:end_index],
    #         #                                                        amounts[iss],
    #         #                                                        )
    #         print(f"Score: {score_of_chunk}")
    #         print()
    #         score *= score_of_chunk

    #     # else:  # combo fail
    #     #     chunks[ic, -1] = 0

    # print("score:")
    # print(score)
    
    # print(chunks)

    # return score


# arrangements = possible_arrangements("???.###", (1,1,3))
# arrangements = possible_arrangements(".??..??...?##.", (1,1,3))
# arrangements = possible_arrangements("?#?#?#?#?#?#?#?", (1,3,1,6))
# arrangements = possible_arrangements("????.#...#...", (4,1,1))
# arrangements = possible_arrangements("????.######..#####.", (1,6,5))
# arrangements = possible_arrangements("?###????????", (3, 2, 1))  # 10




arrangements_per_line = []
for record, amounts in record_lines[5:6]:
    record_arr = make_record_into_array(record)
    arrangements_per_line.append(possible_arrangements(record_arr, amounts))

print(f"Part 2:\n{sum(arrangements_per_line)}")




# print(f"Part 2:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
# print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
