# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

import numpy as np


def parse_input(p_in: str) -> (list, np.array):
    picked_nos_str, *boards_str_list = p_in.split("\n\n")
    picked_nos = [int(val) for val in picked_nos_str.split(",")]

    for z, board_str in enumerate(boards_str_list):
        if z == 0:
            boards = np.empty([len(boards_str_list), 5, 5], dtype="int")
        board = [[int(val) for val in rows.split()]
                 for rows in board_str.split("\n")]
        boards[z, :, :] = np.array(board)

    return picked_nos, boards


def find_winning_boards(picked_nos: list, boards: np.array) -> (np.array, int):
    appeared_mask = np.zeros(boards.shape, dtype=bool)
    winner_boards = []

    # pick numbers
    for turn, number in enumerate(picked_nos):
        appeared_mask += boards == number
        win_mask = np.all(appeared_mask, axis=1) + np.all(appeared_mask, axis=2)
        for board_idx in np.where(win_mask)[0]:
            if board_idx not in [winner["board_idx"] for winner in winner_boards]:
                winning_board = boards[board_idx, :, :]
                unmarked_numbers = winning_board[np.invert(appeared_mask[board_idx, :, :])]
                sum_unmarked = np.sum(unmarked_numbers)
                score = number * sum_unmarked
                winner_boards.append({"board_idx": board_idx, "score": score})
    return winner_boards


solutions = find_winning_boards(*parse_input(p_in))


def part1():
    global solutions
    print("\n--Part 1--")
    print(f"Score: {solutions[0]['score']}")


def part2():
    global solutions
    print("\n--Part 2--")
    print(f"Score: {solutions[-1]['score']}")


part1()
part2()
