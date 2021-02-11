from pathlib import Path

P_IN = Path.cwd().joinpath("input.txt").read_text()

print(sum([len(set(pp)) == len(pp) for pp in
           [line.split() for line in P_IN.splitlines()]]))


# %% Part 2
print(sum([len(set(pp)) == len(pp) for pp in
           [[frozenset(word) for word in line.split()] for line in P_IN.splitlines()]]))
