# 2023 Day 12

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
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

def split_combo_generator(n_sections_cur: int, n_sections_new: int) -> object:
    combos = product(range(n_sections_new + 1), repeat=n_sections_cur)
    gen = (array for array in combos if sum(array) == n_sections_new)
    return gen

def test_split_combo_generator(a, b):
    gen = split_combo_generator(a, b)
    for arr in gen:
        print(arr)

test_split_combo_generator(1, 3)


def possible_arrangements(record_arr, amounts):

    print()
    print("--------", record_arr, amounts)
    split_indexes = [[-1]]
    free_range_indexes = list()
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
                free_range_indexes.append([i, i + 1])
            else:
                free_range_indexes[-1][-1] = i + 1

    # print(f"split_indexes: {split_indexes}")
    print(f"free_range_indexes: {free_range_indexes}")

    scores_per_combo = []
    for n_split__per_section in split_combo_generator(len(free_range_indexes), len(amounts)):
        # e.g. (4, 0, 0, 2)
        print("------split combination:", n_split__per_section)
        scores_per_section = []
        for i_section, n_split in enumerate(n_split__per_section):
            # e.g. section 0, into 4 pieces
            scores_per_offset = []

            if n_split == 0:
                pass
            else:
                print("----section", i_section, ",", n_split, "piece")
                start_index_of_free_range = free_range_indexes[i_section][0]
                end_index_of_free_range = free_range_indexes[i_section][1]
                record_free_range = record_arr[start_index_of_free_range:end_index_of_free_range]
                amounts_start_index = np.sum(n_split__per_section[:i_section], dtype=int)
                amount_new = amounts[amounts_start_index:amounts_start_index+n_split]
                free_play = len(record_free_range) - sum(amount_new) - len(amount_new) + 1
                len_1 = amount_new[0]
                print("record and amount_new:", record_free_range, amount_new)

                # print("--offsets")
                for offset in range(free_play + 1):
                    print("--offset", offset)
                    # why can I not say "== -1" in this next line?
                    if (offset == 0 or all([val == -1 for val in record_free_range[:offset]])) \
                        and (offset + len_1 == len(record_free_range) or record_free_range[offset + len_1] == -1):
                            # if at the beginning or previous elements do not contain 1=="#"
                            # and if at the end or does not contain following elements of 1=="#"
                        scores_per_offset.append(1)
                        
                        if n_split > 1:
                            scores_per_offset[-1] *= possible_arrangements(record_free_range[len_1 + 1 + offset:], amount_new[1:])
                            
                    else:
                        scores_per_offset.append(0)


            print("scores_per_offset: ", scores_per_offset)
            scores_per_section.append(sum(scores_per_offset))

        print("scores_per_section:", scores_per_section)
        scores_per_combo.append(np.prod(scores_per_section, dtype=int))

    print("scores_per_combo:", scores_per_combo)


    return(np.sum(scores_per_combo, dtype=int))



# arrangements = possible_arrangements("???.###", (1,1,3))
# arrangements = possible_arrangements(".??..??...?##.", (1,1,3))
# arrangements = possible_arrangements("?#?#?#?#?#?#?#?", (1,3,1,6))
# arrangements = possible_arrangements("????.#...#...", (4,1,1))
# arrangements = possible_arrangements("????.######..#####.", (1,6,5))
# arrangements = possible_arrangements("?###????????", (3, 2, 1))  # 10


def fold_input(record, amounts, n_fold):
    assert isinstance(record, str)
    assert isinstance(amounts, list)
    return record * n_fold, amounts * n_fold


arrangements_per_line = []
for i, (record, amounts) in enumerate(record_lines):
    folded_record, folded_amounts = fold_input(record, amounts, 5)
    record_arr = make_record_into_array(folded_record)
    arrangements_per_line.append(possible_arrangements(record_arr, folded_amounts))
    print()
    print(f"Solved row {i}: '{folded_record}' {arrangements_per_line[-1]} combinations")
    print(f"Elapsed time: {(perf_counter() - start_time) * 1000:.3g} ms")


print(f"Part 2:\n{arrangements_per_line}")


# print(f"Part 2:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
# print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
