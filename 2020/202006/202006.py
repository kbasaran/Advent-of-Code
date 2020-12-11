# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 08:36:33 2020

@author: kbasa
"""

with open("input.txt") as f:
    # %% Part 1
    Answers, count = [], 0
    for group in f.read().split("\n\n"):
        Answers.append(group.strip())
        chars = Answers[-1].replace("\n", "")
        count += len(set(chars))
    print(count)

# %% Part 2
count = 0
for person in [group.splitlines() for group in Answers]:
    chars = set("".join(person))
    for char in chars:
        count += (1 if all([char in ans for ans in person]) else 0)
print(count)
