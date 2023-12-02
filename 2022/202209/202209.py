# 2022 Day 09

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np

start_time = perf_counter()


def make_rope_segment(head: np.array, tail: np.array) -> np.array:
    return np.array(head) - np.array(tail)

def move_section(head: np.array, tail: np.array) -> np.array:
    "Return new position of tail."
    rope_segment = make_rope_segment(head, tail)
    if any(np.sign(rope_segment) != rope_segment):
        rope_segment_new = rope_segment - np.sign(rope_segment)
    else:
        rope_segment_new = rope_segment.copy()

    return head - rope_segment_new  # tail

def process_command(rope: np.array, command_line: str, visited: set) -> np.array:
    command_parts = command_line.split()
    match command_parts[0]:
        case "U":
            dir_unit_vector = (-1, 0)
        case "D":
            dir_unit_vector = (1, 0)
        case "L":
            dir_unit_vector = (0, -1)
        case "R":
            dir_unit_vector = (0, 1)
    rope_new = rope.copy()
    for _ in range(int(command_parts[1])):
        rope_new[0, :] = rope_new[0, :] + np.array(dir_unit_vector)
        for i_row in range(1, rope.shape[0]):
            # why did np.split return 2D arrays?
            rope_new[i_row, :] = move_section(rope_new[i_row - 1, :], rope_new[i_row, :])
        visited.add(tuple(rope_new[-1, :]))
    return rope_new

def list_all_visited(p_in, rope):
    visited = set()
    rope_new = rope.copy()
    for command_line in p_in.splitlines():
        rope_new = process_command(rope_new, command_line, visited)
    return visited


if __name__ == "__main__":
    rope = np.zeros(4).reshape(2, 2).astype(int)
    print(len(list_all_visited(p_in, rope)))  # Part 1

    rope = np.zeros(20).reshape(10, 2).astype(int)
    print(len(list_all_visited(p_in, rope)))  # Part 2

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
