# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 20:36:57 2021

@author: kbasa
"""

from pathlib import Path

P_IN = Path.cwd().joinpath("input.txt").read_text()


def part1rule(digits):
    sum = 0
    for i, digit in enumerate(digits):
        if digit == digits[(i + 1) % len(digits)]:
            sum += int(digit)
    return sum


def part2rule(digits):
    half_way_length = int(len(digits) / 2)
    sum = 0
    for i in range(len(digits)):
        if digits[i] == digits[(i + half_way_length) % len(digits)]:
            sum += int(digits[i])
    return sum


result1 = part1rule(P_IN)
result2 = part2rule(P_IN)

print(f"Result: {result1}")
print(f"Result: {result2}")
