# 2022 Day 01
# Take input
with open('input.txt') as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

food_list_per_elf = [[int(food) for food in elf.split("\n")] for elf in p_in.split("\n\n")]

# Part 1
cal_per_elf = [sum(food_list) for food_list in food_list_per_elf]
print(max(cal_per_elf))

# Part 2
print(sum(sorted(cal_per_elf)[-3:]))

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
