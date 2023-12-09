# 2023 Day 08

# Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from functools import lru_cache

start_time = perf_counter()

# ---- Part 1

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@lru_cache
def convert_to_number(loc: str) -> int:
    assert len(loc) == 3
    base = len(letters)
    values = [base**i * letters.find(letter) for i, letter in enumerate(reversed(loc))]
    assert all([value >= 0 for value in values])
    return sum(values)

@lru_cache
def convert_to_name(number: int) -> str:
    base = len(letters)
    orders = [-1] * 3
    orders[0], rest = divmod(number, base**2)
    orders[1], rest = divmod(rest, base**1)
    orders[2] = rest
    print(orders)
    return letters[orders[0]] + letters[orders[1]] + letters[orders[2]]


print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
