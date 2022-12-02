# 2022 Day 02
# Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np

start_time = perf_counter()

# rows are opponent's hand, columns are your
win_mat = np.matrix([[3, 6, 0],
                     [0, 3, 6],
                     [6, 0, 3],
                     ]) + np.matrix([1, 2, 3]).repeat(3, axis=0)


def convert_letters_to_coords(row_text):
    l1, l2 = row_text.split(" ")
    row_no = "ABC".find(l1)
    col_no = "XYZ".find(l2)
    return row_no, col_no


# Part 1
tot_score = 0
for row_text in p_in.splitlines():
    tot_score += win_mat[convert_letters_to_coords(row_text)]
print(tot_score)

# Part 2
score_mat = np.matrix([[3, 1, 2],
                       [1, 2, 3],
                       [2, 3, 1],
                       ]) + np.matrix([0, 3, 6]).repeat(3, axis=0)

tot_score = 0
for row_text in p_in.splitlines():
    tot_score += score_mat[convert_letters_to_coords(row_text)]
print(tot_score)


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
