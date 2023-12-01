# 2023 Day 01

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import string

start_time = perf_counter()

# --- Part 1
def solve_part_1(p_in):
    p_in_digit_only = "".join([val for val in p_in if val in (string.digits + "\n")])
    calibration_vals = [10 * int(line[0]) + int(line[-1]) for line in p_in_digit_only.splitlines()]

    print(sum(calibration_vals))


solve_part_1(p_in)
print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")

# --- Part 2
text_to_int = {"one": 1,
               "two": 2,
               "three": 3,
               "four": 4,
               "five": 5,
               "six": 6,
               "seven": 7,
               "eight": 8,
               "nine": 9,
               }

p_in_translated = p_in

for text_val, int_val in text_to_int.items():
    p_in_translated = p_in_translated.replace(text_val, text_val[0] + str(int_val) + text_val[-1])

solve_part_1(p_in_translated)
print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
