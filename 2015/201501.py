# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:21:41 2020

@author: kerem.basaran
"""

import pandas as pd

def move(instr, start=0):
    pos=start
    for char_order, step in enumerate(instr):
        if step == "(": 
            pos += 1
        elif step == ")":
            pos -= 1
        else:
            raise Exception(f"invalid input: {step}")
        if pos == -1:
            print(f"In basement at character: {char_order+1}")
    return(pos)

puzzle_input = pd.read_clipboard().columns[0]
print(move(puzzle_input))
