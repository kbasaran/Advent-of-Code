# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:35:02 2020

@author: kerem.basaran
"""

import pyperclip
import numpy as np
import pandas as pd

puzzle_input = pyperclip.paste()
str_len = len(puzzle_input)

df_santa = pd.DataFrame(np.nan, index=range(str_len), columns=["x", "y"])
df_santa.iloc[0, :] = [0, 0]
df_robo = df_santa.copy(deep=True)


# %%
def move(df, ind, instr):
    """Move the guys to the next house."""
    global df_santa, df_robo
    x, y = df.iloc[[ind+1]]
    if instr == "^":
        df.iloc[[ind+2]] = [[x, y+1]]
    elif instr == "v":
        df.iloc[[ind+2]] = [[x, y-1]]
    elif instr == "<":
        df.iloc[[ind+2]] = [[x-1, y]]
    elif instr == ">":
        df.iloc[[ind+2]] = [[x+1, y]]
    else:
        raise Exception(f"Invalid instruction: {instr}")


for i, instr in enumerate(puzzle_input):
    if i % 2 == 0:
        move(df_santa, i, instr)
    else:
        move(df_robo, i, instr)

df_tot = df_santa.append(df_robo).dropna()

pt = df_tot.pivot_table(index=["x", "y"], aggfunc="size")
print(pt[pt > 0].count())
