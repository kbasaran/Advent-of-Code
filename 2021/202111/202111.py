# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product
import numpy as np

start_time = perf_counter()


def parse_input(p_in):
    rows = []
    for row in p_in.splitlines():
        rows.append([int(val) for val in row])
    octopi = np.array(rows,
                      dtype=np.intp,
                      )
    return octopi


def find_neighbour_coords(coord, array_shape) -> set:
    neighbour_mask = list(product([-1, 0, 1], repeat=2))
    neighbour_mask.pop(4)  # pop (0, 0)
    neighbour_coords = set()
    for x, y in neighbour_mask:
        new_coord = (x + coord[0], y + coord[1])
        if all([(coord > -1 and coord < array_shape[axis]) for axis, coord in enumerate(new_coord)]):
            neighbour_coords.add((new_coord))
    return neighbour_coords


def execute_step(octopi):
    flashes = 0
    octopi = octopi + 1
    exploders = set()
    while octopi[octopi > 9].size > 0:
        ans_x, ans_y = np.where(octopi > 9)
        for i in range(ans_x.size):
            coord = ans_x[i], ans_y[i]
            exploders.add(coord)
            for neighbour in find_neighbour_coords(coord, octopi.shape):
                octopi[neighbour] += 1
            octopi[coord] = 0
            flashes += 1

    exploder_coords = ([val[0] for val in exploders], [val[1] for val in exploders])
    octopi[exploder_coords] = 0

    return octopi, flashes


def part_1(p_in):
    octopi = parse_input(p_in)
    flashes_total = 0
    for step in range(1, 101):
        octopi, flashes = execute_step(octopi)
        flashes_total += flashes
    print(f"\n--Part 1--\nAnswer: {flashes_total}")


def part_2(p_in):
    octopi = parse_input(p_in)
    step = 0
    while True:
        step += 1
        octopi, flashes = execute_step(octopi)
        if flashes == np.product(octopi.shape):
            print(f"\n--Part 2--\nAnswer: {step}")
            break


part_1(p_in)
part_2(p_in)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
