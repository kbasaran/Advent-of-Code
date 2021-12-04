# %% Take input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

# Code here

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
