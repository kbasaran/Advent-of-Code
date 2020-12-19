# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:27:32 2020

@author: kerem.basaran
"""

import numpy as np
import time

p_in = [6, 19, 0, 5, 7, 13, 1]

start = time.time()
turn_amount = 30_000_000

# Storage matrix. Cols are the numbers that get spoken.
# The two rows represent the last two encounters the number has been spoken
# Cell value is the turn at which the number has been spoken
nf = np.full((2, turn_amount), -1, dtype=np.int32)
spoken = -1
turn = 0


def new_turn(predefined=-1):
    global nf, spoken, turn
    turn += 1

    last_spoken_val = spoken

    if predefined >= 0:  # first numbers read from a list
        spoken = predefined

    elif last_spoken_val >= 0:  # otherwise
        if nf[1, last_spoken_val] == -1:  # last spoken was spoken for the first time
            spoken = 0
        else:  # last spoken was spoken more than once before
            spoken = nf[0, last_spoken_val] - nf[1, last_spoken_val]

    nf[1, spoken] = nf[0, spoken]
    nf[0, spoken] = turn


# Loop through first turns they read from a list
for val in p_in:
    new_turn(val)

# Do the other turns where they actually
for _ in range(turn_amount - len(p_in)):
    new_turn()

print(f"Elapsed: {time.time()-start:.4f}s")
print(f"Turn: {turn}, Spoken: {spoken}")
