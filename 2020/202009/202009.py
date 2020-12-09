from itertools import combinations

with open("input.txt") as f:
    p_in = [int(i) for i in f.read().splitlines()]

# %% Part 1
preamble_len = 25
for i, number in enumerate(p_in):
    if i > preamble_len - 1:
        valid = number in [sum(comb) for comb in combinations(p_in[i-25:i], 2)]
        if not valid:
            print(f"Line: {i} Value: {number} is not valid.")

# %% Part 2
target = 1639024365
for i_start in range(len(p_in) - 2):
    i = i_start + 2
    while i < len(p_in):
        numbers = p_in[i_start:i]
        sum_numbers = sum(numbers)
        valid = (sum_numbers == target)
        if valid:
            answer = min(numbers) + max(numbers)
            print(f"Pos {i_start+1} and Pos {i} => Sum is {answer}")
        if sum_numbers > target:
            break
        i += 1
