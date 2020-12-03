# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:35:02 2020

@author: kerem.basaran
"""

import pyperclip
import numpy as np
import pandas as pd

df_santa = pd.DataFrame({"x": [0], "y": [0]})
df_robo = pd.DataFrame({"x": [0], "y": [0]})

def move(df, instr):
    pos = df.iloc[-1,:].copy()
    if instr == "^":
        pos["y"] += 1
    elif instr == "v":
        pos["y"] += -1
    elif instr == "<":
        pos["x"] += -1
    elif instr == ">":
        pos["x"] += 1
    else:
        raise Exception(f"Invalid instruction: {instr}")
    return df.append(pos, ignore_index=True)

puzzle_input = pyperclip.paste()

for i, instr in enumerate(puzzle_input):
    if i % 2 == 0:
        df_santa = move(df_santa, instr)
    else:
        df_robo = move(df_robo, instr)

df_tot = df_santa.append(df_robo)

pt = df_tot.pivot_table(index=["x", "y"], aggfunc="size")
print(pt[pt>0].count())
