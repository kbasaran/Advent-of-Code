# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:03:32 2020

@author: kbasa
"""
import numpy as np
import time
import winsound

tic = time.perf_counter()
target_gift_amount = 29000000

received_gifts = np.zeros(10000, dtype=np.int32)
# array for storing number of gifts from each elf for a given house


def calc_n_gift_to_house(house_no):
    """Calculate how many gifts are delivered to a given house."""
    global received_gifts

    # Grow the received gifts array if necessary
    required_array_size = int(2**np.ceil(np.log2(house_no + 1)))
    if required_array_size > len(received_gifts):
        received_gifts = np.zeros(required_array_size)
        print(f"Increased array size to: {required_array_size}")

    # Fill in the array with gift amounts from each elf
    received_gifts[:] = 0
    for elf_no in range(1, house_no+1):
        if house_no % elf_no == 0:
            received_gifts[elf_no] = int(elf_no * 10)
    return sum(received_gifts)


house_no = 0
while 1:
    house_no += 1
    if (n_gifts := calc_n_gift_to_house(house_no)) >= target_gift_amount:
        print(f"{n_gifts} gifts to house {house_no}")
        toc = time.perf_counter()
        break

print(f"Elapsed time: {toc - tic:0.2f} seconds")
winsound.Beep(2000, 1000)
