# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 16:09:37 2020

@author: kbasa
"""

P_IN = "614752839"
cups = [int(i) for i in P_IN]
min_cup_val = min(cups)
max_cup_val = max(cups)
import time
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 220
# dest_cup_trend = []

def do_move(cups):
    global min_cup_val, max_cup_val, dest_cup_trend
    current_val = cups[0]
    removed = cups[1:4]
    new_cups = [cups[0]] + cups[4:]

    dest_cup_val = current_val - 1
    if dest_cup_val < min_cup_val:
        dest_cup_val = max_cup_val
    while dest_cup_val in removed:
        dest_cup_val -= 1
        if dest_cup_val < min_cup_val:
            dest_cup_val = max_cup_val
    
    dest_cup_pos = new_cups.index(dest_cup_val)
    # dest_cup_trend.append(dest_cup_pos)
    new_cups = new_cups[:dest_cup_pos+1] + removed + new_cups[dest_cup_pos+1:]
    new_cups = new_cups[1:] + [new_cups[0]]
    return new_cups

for _ in range(100):
    cups = do_move(cups)

index_one = cups.index(1)
cups_after_one = cups[index_one+1:] + cups[:index_one]
print("Part 1 Answer:")
print("".join([str(i) for i in cups_after_one]))

# %% Part 2
print("--Part 2--")
import numpy as np
start = time.time()
P_IN = "614752839"
# P_IN = "389125467"
P_IN_MAX = max([int(i) for i in P_IN])
cups = np.array([int(i) for i in P_IN] + list(range(P_IN_MAX + 1, 1_000_000 + P_IN_MAX - len(P_IN) + 1)), dtype="int32")
min_cup_val = np.min(cups)
max_cup_val = np.max(cups)
curr_pos = 0

def do_move_fast(cups):
    global min_cup_val, max_cup_val, curr_pos
    # print(curr_pos, cups)
    current_val = cups[curr_pos]
    p2 = cups[curr_pos+1:curr_pos+4]
    # new_cups = cups[:curr_pos+1] + cups[curr_pos+4:]

    dest_cup_val = current_val - 1
    if dest_cup_val < min_cup_val:
        dest_cup_val = max_cup_val
    while dest_cup_val in p2:
        dest_cup_val -= 1
        if dest_cup_val < min_cup_val:
            dest_cup_val = max_cup_val

    # dest_cup_pos = curr_pos + cups[curr_pos:].index(dest_cup_val)
    if curr_pos > 4:
        dest_cup_pos = len(cups) - 4
    else:
        dest_cup_pos = np.where(cups == dest_cup_val)[0][0]
    # print(dest_cup_pos)
    if (curr_pos % 999900 == 0) or (dest_cup_pos < curr_pos):
        cups = np.concatenate([cups[curr_pos:], cups[:curr_pos]])
        dest_cup_pos = (dest_cup_pos - curr_pos) % len(cups)
        curr_pos = 0

    # dest_cup_trend.append(dest_cup_pos)
    p2_start = curr_pos + 1
    p3_start = curr_pos + 4
    # rest_start = dest_cup_pos + 1
    # p1 = cups[:curr_pos+1]
    p3 = cups[p3_start:dest_cup_pos]
    # rest = cups[rest_start:]
    # new_cups = p1 + p3 + [dest_cup_val] + p2 + rest
    cups[p2_start:(p2_start + len(p3) + 1 + 3)] = np.concatenate([p3, np.array([dest_cup_val]), p2])
    # cups[p2_start:(p2_start + len(p3))] = p3
    # cups[(p2_start + len(p3))] = dest_cup_val
    # cups[(p2_start + len(p3) + 1):(p2_start + len(p3) + 1 + 3)] = p2
    # new_cups = new_cups[:dest_cup_pos+1] + p2 + new_cups[dest_cup_pos+1:]
    # new_cups = new_cups[curr_pos+1:] + [new_cups[curr_pos]]
    curr_pos = curr_pos + 1
    return cups


# plt.figure()
# plt.subplot(111)

for move_count in range(10_000_000):
    # plt.plot(cups, label=("Turn " + str(move_count)))

    if move_count % 10_000 == 0 and (move_count > 0):
        print(f"{move_count / 10_000_000 * 100:.2f}% finished.")
        print(f"    Expected total time: {(time.time() - start) / move_count * 10e6 / 60 / 60:.2f} hours")
    cups = do_move_fast(cups)

# plt.grid()
# plt.legend()
# plt.xlabel("location of cup (current cup = 0)")
# plt.ylabel("label of cup")
# plt.show()

index_one = np.where(cups == 1)[0][0]
cups = np.concatenate([cups[index_one:], cups[:index_one]])
two_cups_next_to_one = cups[1:3]
cups_after_one = cups[1:]
# print("Part 1 Check shold be 89372645 for 100 turns:")
# print("".join([str(i) for i in cups_after_one]))
print("Part 2 Answer:")
print(two_cups_next_to_one)
print(two_cups_next_to_one[0] * two_cups_next_to_one[1])

# plt.plot(dest_cup_trend)
