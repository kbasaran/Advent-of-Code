# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:03:32 2020

@author: kbasa
"""
import numpy as np
import time
import winsound
import numba as nb


# %% Part 1
tic = time.perf_counter()
target_gift_amount = 29000000


@nb.njit(parallel=True)
def calc_n_gift_to_house(house_no):
    """Calculate how many gifts are delivered to a given house."""
    elves = np.arange(1, house_no+1)
    gifts = elves[np.mod(house_no, elves) == 0] * 10
    return np.sum(gifts)


house_no = 0
while 1:
    house_no += 1
    if np.mod(house_no, 2**16) == 0:
        print(f"At house: {house_no}")
    if (n_gifts := calc_n_gift_to_house(house_no)) >= target_gift_amount:
        print(f"{n_gifts} gifts to house {house_no}")
        toc = time.perf_counter()
        break

print(f"Elapsed time: {toc - tic:0.2f} seconds")
winsound.Beep(2000, 1000)


# %% Part 2
tic = time.perf_counter()
target_gift_amount = 29000000


@nb.njit(parallel=True)
def calc_n_gift_to_house(elf_no):
    """Calculate how many gifts are delivered to a given house."""
    elves = np.arange(1, house_no+1)
    gifts = elves[np.mod(house_no, elves) == 0][:50] * 11
    return np.sum(gifts)


house_no = 0
while 1:
    house_no += 1
    if np.mod(house_no, 2**16) == 0:
        print(f"At house: {house_no}")
    if (n_gifts := calc_n_gift_to_house(house_no)) >= target_gift_amount:
        print(f"{n_gifts} gifts to house {house_no}")
        toc = time.perf_counter()
        break

print(f"Elapsed time: {toc - tic:0.2f} seconds")
winsound.Beep(2000, 1000)
