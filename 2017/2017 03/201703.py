import time

tic = time.perf_counter()

P_IN = 368078

pos_dict = {1: (0, 0)}
dirt = -1j  # direction
for pos_val in range(1, P_IN+1):
    x, y = pos_dict[pos_val]

    if x == y or (x > 0 and x - 1 == -y) or (x < 0 and -x == y):
        dirt *= 1j  # gives a float

    pos_dict[pos_val + 1] = (int(x + dirt.real), int(y + dirt.imag))

ans_pos = pos_dict[P_IN]

toc = time.perf_counter()

print(f"Part 1: {sum([abs(val) for val in ans_pos])}")
print(f"Elapsed time:{toc-tic:.4f}s")

# %% Part 2
from itertools import product

tic = time.perf_counter()

neighbour_mask = list(product([-1, 0, 1], repeat=2))
new_dict = {val: 0 for val in pos_dict.values()}  # reverse map the dictionary
new_dict[(0, 0)] = 1

for pos_val in sorted(pos_dict.keys()):
    coord = pos_dict[pos_val]
    value_to_write = sum([new_dict[(coord[0]+mask[0], coord[1]+mask[1])]
                          for mask in neighbour_mask])
    if value_to_write > P_IN:
        break
    else:
        new_dict[coord] = value_to_write

toc = time.perf_counter()

print()
print(f"Part 2: {value_to_write}")
print(f"Elapsed time:{toc-tic:.4f}s")
