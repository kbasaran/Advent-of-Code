# 2022 Day 02
# Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
from functools import lru_cache

start_time = perf_counter()


# Part 1
@lru_cache
def convert_letters_to_coords(row_text):
    l1, l2 = row_text.split(" ")
    row_no = "ABC".find(l1)
    col_no = "XYZ".find(l2)
    return row_no, col_no


def process_strategy_guide(p_in, score_matrix):
    tot_score = 0
    for row_text in p_in.splitlines():
        tot_score += score_matrix[convert_letters_to_coords(row_text)]
    print(tot_score)


# rows are opponent's hand, columns are your
win_mat = np.matrix([[3, 6, 0],
                     [0, 3, 6],
                     [6, 0, 3],
                     ]) + np.matrix([1, 2, 3]).repeat(3, axis=0)

process_strategy_guide(p_in, win_mat)

# Part 2
p2_mat = np.matrix([[3, 1, 2],
                    [1, 2, 3],
                    [2, 3, 1],
                    ]) + np.matrix([0, 3, 6]).repeat(3, axis=0)

process_strategy_guide(p_in, p2_mat)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
