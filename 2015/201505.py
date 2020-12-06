# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 23:05:14 2020

@author: kbasa
"""

import pyperclip

p_in = pyperclip.paste().splitlines()


# %% Part 1
def nice(string):
    valid = 0

    count_w = 0
    for w in "aeiou":
        count_w += string.count(w)
    if count_w >= 3:
        valid += 1

    for i in range(1, len(string)):
        if string[i-1] == string[i]:
            valid += 2
            break

    if not any([(bad in string) for bad in ["ab", "cd", "pq", "xy"]]):
        valid += 4

    return valid == 8 - 1


nice_ones = []
for string in p_in:
    nice_ones.append(nice(string))

print(nice_ones.count(True))


# %% Part 2
def nice_2(string):
    valid = 0

    for i in range(1, len(string)-1):
        pair = string[i-1:i+1]
        if string.count(pair) > 1 and \
                (len(string.replace(pair, "  ")) <= len(string)):
            valid += 1
            break

    for i in range(2, len(string)):
        if string[i-2] == string[i]:
            valid += 2
            break
    return valid == 4 - 1


nice_ones_2 = []
for string in p_in:
    nice_ones_2.append(nice_2(string))

print(nice_ones_2.count(True))
