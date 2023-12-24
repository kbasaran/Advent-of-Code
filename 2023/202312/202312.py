# 2023 Day 12

# ---- Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
import numpy as np
from functools import lru_cache, cache

# ---- Part 1
start_time = perf_counter()


def parse_input(p_in):
    record_lines = []
    for line in p_in.strip().splitlines():
        record, amounts_str = line.split()
        record_lines.append((record, tuple([int(val) for val in amounts_str.split(",")])))

    return record_lines  # tuple of record and amount


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
# arrangements_per_line = []
# for record, amounts in record_lines:
#     arrangements_per_line.append(possible_arrangements(record, amounts))

# print(f"Part 1:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
# print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2
start_time = perf_counter()


def make_record_into_tuple(record):
    record_with_digits = record.replace("?", "0").replace(".", "1").replace("#", "2")
    record_w_digits = tuple([int(val) - 1 for val in record_with_digits])
    # -1 is the question marks
    return record_w_digits


def split_combo_generator(n_sections_cur: int, n_sections_new: int) -> object:
    combos = product(range(n_sections_new + 1), repeat=n_sections_cur)
    gen = (array for array in combos if sum(array) == n_sections_new)
    return gen


@cache
def split_combos(n_sections_cur: int, n_sections_new: int) -> object:
    gen = split_combo_generator(n_sections_cur, n_sections_new)
    return tuple(list(gen))


def test_split_combo_generator(a, b):
    gen = split_combo_generator(a, b)
    for arr in gen:
        print(arr)

# test_split_combo_generator(1, 3)


@cache
def arrangements_per_section(record_single, amount_new):
    free_play = len(record_single) - sum(amount_new) - len(amount_new) + 1
    len_1 = amount_new[0]
    # print("record and amount_new:", record_single, amount_new)

    section_score = 0
    for offset in range(free_play + 1):
        # print("--offset", offset)
        if (offset == 0 or all([val == -1 for val in record_single[:offset]])) \
            and (offset + len_1 == len(record_single) or record_single[offset + len_1] == -1):
                # if at the beginning or previous elements do not contain 1=="#"
                # and if at the end or does not contain following elements of 1=="#"
            section_score += 1

            if len(amount_new) > 1:
                section_score += -1 + possible_arrangements(record_single[len_1 + 1 + offset:], amount_new[1:])

    return section_score


@cache
def possible_arrangements(record_w_digits, amounts):

    # print()
    # print("--------", record_w_digits, amounts)
    free_range_indexes = list()
    for i, val in enumerate(record_w_digits):
        val_prev = 0 if i == 0 else record_w_digits[i-1]

        if val == 1 or val == -1:
            if val_prev == 0:
                free_range_indexes.append([i, i + 1])
            else:
                free_range_indexes[-1][-1] = i + 1

    # print(f"free_range_indexes: {free_range_indexes}")

    end_score = 0
    for n_split__per_section in split_combos(len(free_range_indexes), len(amounts)):
        # e.g. (4, 0, 0, 2)
        # print("------split combination:", n_split__per_section)
        combo_score = 1
        for i_section, n_split in enumerate(n_split__per_section):
            # e.g. section 0, into 4 pieces

            if n_split == 0:
                section_score = 1
            else:
                # print("----section", i_section, ",", n_split, "piece")
                start_index_of_free_range = free_range_indexes[i_section][0]
                end_index_of_free_range = free_range_indexes[i_section][1]
                record_free_range = record_w_digits[start_index_of_free_range:end_index_of_free_range]
                amounts_start_index = sum(n_split__per_section[:i_section])
                amount_new = amounts[amounts_start_index:amounts_start_index+n_split]

                section_score = arrangements_per_section(record_free_range, amount_new)

            # print("section_score: ", section_score)
            combo_score *= section_score

        # print("combo_score:", combo_score)
        end_score += combo_score

    # print("end_score:", end_score)
    return end_score


def fold_input(record, amounts, n_fold):
    assert isinstance(record, str)
    assert isinstance(amounts, tuple)
    return ((record + "?") * n_fold)[:-1], amounts * n_fold


arrangements_per_line = []
for i, (record, amounts) in enumerate(record_lines):
    start_compute_time = perf_counter()
    folded_record, folded_amounts = fold_input(record, amounts, 2)
    record_w_digits = make_record_into_tuple(folded_record)
    arrangements_per_line.append(possible_arrangements(record_w_digits, folded_amounts))
    print()
    print(f"Solved row {i}: '{folded_record}' {arrangements_per_line[-1]} combinations")
    print(f"Compute time: {(perf_counter() - start_compute_time):.3g} s")


print(f"Part 2:\n{arrangements_per_line}")


# print(f"Part 2:\n{sum([len(arrangement) for arrangement in arrangements_per_line])}")
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
