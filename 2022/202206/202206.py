# 2022 Day 06

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

def find_pos_sop_marker(data, length):
    for i in range(1, len(data)+1):
        if len(set(data[i-length:i])) == length:
            return i
    raise ValueError("Not found")

print(find_pos_sop_marker(p_in, 4))
print(find_pos_sop_marker(p_in, 14))


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
