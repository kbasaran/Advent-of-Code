# 2022 Day 10

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

start_time = perf_counter()

def run_cycle(instructions, i_cycle, X) -> (int, str):
    "Returns X value after this cycle (not during!)"
    if i_cycle == 1:
        return X
    elif instructions[i_cycle - 2][0] == "a":  # previous item in list
        return X + int(instructions[i_cycle - 1])
    else:
        return X


if __name__ == "__main__":
    instructions = p_in.replace("\n", " ").split()
    X = 1
    sig_strengths = []
    image = np.full(240, False)
    for i_cycle in range(1, len(instructions)+1):

        # Part 1
        if i_cycle % 40 == 20:
            sig_strengths.append(X * i_cycle)

        # Part 2
        i_draw = i_cycle - 1
        # print(f"during {i_cycle}, CRT draws in position {i_draw}, starting X is {X}")
        if i_draw % 40 in list(range(X-1, X+2)):
            image[i_draw] = True

        X = run_cycle(instructions, i_cycle, X)

    print(sum(sig_strengths))  # Part 1
    plt.matshow(image.reshape((6, 40)))  # Part 2

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
