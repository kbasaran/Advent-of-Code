# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

start_time = perf_counter()


def translate_coords(coord_x, coord_y) -> tuple:
    row, col = coord_x, coord_y
    return col, row


def parse_input(p_in: str) -> np.array:
    map_text, fold_text = p_in.split("\n\n")
    y_max = max([int(val.split(",")[0]) for val in map_text.splitlines()])
    x_max = max([int(val.split(",")[1]) for val in map_text.splitlines()])

    paper = np.full([x_max + 1, y_max + 1], False)
    for row_text in map_text.splitlines():
        y, x = [int(val) for val in row_text.split(",")]
        paper[x, y] = True

    instr = []
    for row_text in fold_text.splitlines():
        fold_idx = int(row_text[13:])
        fold_type = row_text[11]
        instr.append((fold_type, fold_idx))

    return np.array(paper), instr


def fold(paper, fold_type, fold_idx) -> np.array:
    if fold_type == "y":
        upper_side = paper[:fold_idx, :]
        lower_side = np.flipud(paper[fold_idx+1:, :])
        row_len_difference = upper_side.shape[0] - lower_side.shape[0]
        if row_len_difference > 0:
            # bottom side is smaller
            upper_side[row_len_difference:, :] += lower_side
            return upper_side
        else:
            lower_side[-row_len_difference:, :] += upper_side
            return lower_side
    elif fold_type == "x":
        left_side = paper[:, :fold_idx]
        right_side = np.fliplr(paper[:, fold_idx+1:])
        col_len_difference = left_side.shape[1] - right_side.shape[1]
        if col_len_difference > 0:
            # right side is smaller
            left_side[:, col_len_difference:] += right_side
            return left_side
        else:
            right_side[:, -col_len_difference:] += left_side
            return right_side


def part_1(p_in):
    folded_paper, fold_instr = parse_input(p_in)
    fold_type, fold_idx = fold_instr[0]
    folded_paper = fold(folded_paper, fold_type, fold_idx)
    print(f"\n--Part 1--\nAnswer: {len(folded_paper[folded_paper])}")
    return folded_paper


def part_2(p_in):
    folded_paper, fold_instr = parse_input(p_in)
    for fold_type, fold_idx in fold_instr:
        folded_paper = fold(folded_paper, fold_type, fold_idx)
    plt.imshow(folded_paper)
    plt.title("202113")
    return folded_paper


part_1(p_in)
part_2(p_in)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
