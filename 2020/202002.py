# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 08:53:05 2020

@author: kerem.basaran
"""

import pandas as pd

# Read puzzle input
df = pd.read_clipboard(sep=" ", header=None)
df.columns = ["min_max", "key_letter", "password"]
df["key_letter"] = df["key_letter"].str[:-1]
df["min_max"] = df["min_max"].str.split("-")


# %% Part 1
def pass_part_1(entry):
    min, max = [int(i) for i in entry.min_max]
    occurrence = entry.password.count(entry.key_letter)
    return (True if min <= occurrence <= max else False)


print(df.apply(pass_part_1, axis=1).value_counts())


# %% Part 2
def pass_part_2(entry):
    letters = [entry.password[int(i)-1] for i in entry.min_max]
    return (True if letters.count(entry.key_letter) == 1 else False)


print(df.apply(pass_part_2, axis=1).value_counts())
