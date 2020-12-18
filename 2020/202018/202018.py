# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:27:38 2020

@author: kerem.basaran
"""

import numpy as np

with open("input.txt") as f:
    p_in = f.read().splitlines()


def calculate_with_left_operation_first(string):
    strl = string.strip("()").split(" ")
    while len(strl) > 1:
        if strl[1] == "*":
            val = int(strl[0]) * int(strl[2])
        elif strl[1] == "+":
            val = int(strl[0]) + int(strl[2])
        strl = [val] + strl[3:]
    return int(strl[0])


def do_operation_in_deepest_parentheses(string):
    pos = [0, len(string) - 1]
    for i, char in enumerate(string):
        if char == "(":
            pos[0] = i
        if char == ")":
            pos[1] = i
            break

    calculated = calculate_with_left_operation_first(string[pos[0]:pos[1]+1])
    return string[:pos[0]] + str(calculated) + string[pos[1]+1:]

def solve_a_line(line):
    string = line
    while "(" in string:
        string = do_operation_in_deepest_parentheses(string)
    return calculate_with_left_operation_first(string)


# Go through the puzzle input and sum the results
sum_lines = 0
for line in p_in:
    sum_lines += solve_a_line(line)

print(sum_lines)


# %% Part 2
def calculate_with_addition_first(string):
    strl = string.strip("()").split(" ")
    # Do all the addition operations
    while "+" in strl:
        for i, chars in enumerate(strl):
            if chars == "+":
                pos = [i-1, i+1]
                val = np.sum([np.int64(strl[i]) for i in pos])
                strl = strl[:pos[0]] + [val] + strl[pos[1]+1:]
                break

    # Take product of all the rest (after removing the * signs from in betweens)
    multips = np.prod([np.int64(val) for val in strl if val != "*"])
    return multips


def do_operation_in_deepest_parentheses_p2(string):
    pos = [0, len(string) - 1]
    for i, char in enumerate(string):
        if char == "(":
            pos[0] = i
        if char == ")":
            pos[1] = i
            break

    calculated = calculate_with_addition_first(string[pos[0]:pos[1]+1])
    return string[:pos[0]] + str(calculated) + string[pos[1]+1:]


def solve_a_line_p2(line):
    string = line
    while "(" in string:
        string = do_operation_in_deepest_parentheses_p2(string)
    return calculate_with_addition_first(string)


# Go through the puzzle input and sum the results
sum_lines = 0
for line in p_in:
    sum_lines += solve_a_line_p2(line)
    
print(sum_lines)
