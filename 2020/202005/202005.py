# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 06:37:02 2020

@author: kbasa
"""

with open("input.txt") as f:
    Bpss = f.read().splitlines()

# %% Part 1
def row_no(bps):
    return int(bps[:7].replace("F", "0").replace("B", "1"), 2)

def col_no(bps):
    return int(bps[7:].replace("L", "0").replace("R", "1"), 2)

def sid(bps):
    return row_no(bps) * 8 + col_no(bps)


seats = []
for bps in Bpss:
    seats.append((row_no(bps), col_no(bps), sid(bps)))

print(max([i[2] for i in seats]))


# %% Part 2
def seat_order(bps):
    return row_no(bps) * 2**3 + col_no(bps)

seat_vals = sorted([seat_order(bps) for bps in Bpss])

for i in range(1, len(seat_vals)-1):
    if seat_vals[i] != seat_vals[i-1] + 1:
        print(seat_vals[i]-1)
