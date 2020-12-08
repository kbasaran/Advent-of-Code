# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:00:17 2020

@author: kbasa
"""

with open("input.txt") as f:
    p_in = f.read().splitlines()

# %% Part 1
def find_loop(p_in: list) -> int:
    curr_line, accum = 0, 0
    visited_lines = []
    for _ in range(99999):
        if curr_line in visited_lines:
            return accum
        visited_lines.append(curr_line)

        # Process instructions
        comm, val = p_in[curr_line].split(" ")

        if comm == "acc":
            accum += int(val)

        if comm == "jmp":
            curr_line += int(val) -1

        curr_line += 1

print(f"Loop starts when accumulator is: {find_loop(p_in)}")

# %% Part 2
def switch_nop_jmp(comm):
    if comm == "jmp":
        return "nop"
    elif comm == "nop":
        return "jmp"
    else:
        return comm

def find_loop_or_end(p_in: list, line_to_replace: int) -> int:
    curr_line, accum = 0, 0
    visited_lines = []
    for _ in range(99999):
        if (curr_line in visited_lines) or (curr_line >= len(p_in)):
            return
        visited_lines.append(curr_line)

        # Process instructions
        comm, val = p_in[curr_line].split(" ")
        if curr_line == line_to_replace:
            comm = switch_nop_jmp(comm)

        if comm == "acc":
            accum += int(val)

        if curr_line == len(p_in) - 1:
            return accum

        if comm == "jmp":
            curr_line += int(val) -1

        curr_line += 1

for line_to_replace in range(len(p_in)):
    accum = find_loop_or_end(p_in, line_to_replace)
    if accum:
        print(f"Replaced line: {line_to_replace} and reached the end. Accumulator is: {accum}")

