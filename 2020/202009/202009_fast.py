from itertools import combinations
import time

start1 = time.time()
with open("input.txt") as f:
    p_in = [int(i) for i in f.read().splitlines()]

# %% Part 1
preamble_len = 25
for i, number in enumerate(p_in):
    if i > preamble_len - 1:
        valid = number in [sum(comb) for comb in combinations(p_in[i-25:i], 2)]
        if not valid:
            print(f"Line: {i} Value: {number} is not valid.")

print(f"Time: {time.time()-start1:.3f}s")
start2 = time.time()
# %% Part 2
target = 1639024365

i_start, i = 0, 2
dir = 1  # direction i index (upper limit) is moving
while i < len(p_in):
    numbers = p_in[i_start:i]
    sum_numbers = sum(numbers)

    if (dir == 1) & (sum_numbers < target):
        i += 1

    elif (dir == 1) & (sum_numbers > target):
        i_start += 1
        dir = -1

    elif (dir == -1) & (sum_numbers > target):
        i += -1

    elif (dir == -1) & (sum_numbers < target):
        i_start += 1
        dir = 1

    elif sum_numbers == target:
        answer = min(numbers) + max(numbers)
        print(f"Pos {i_start+1} and Pos {i} => Sum is {answer}")
        break

    else:
        print(f"Error at: {i_start, i, dir}")
print(f"Time: {time.time()-start2:.3f}s")
