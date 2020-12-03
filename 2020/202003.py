# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 12:29:26 2020

@author: kerem.basaran
"""

import pyperclip
import numpy as np

puzzle_input = pyperclip.paste().replace(".", "0").replace("#", "1")

Field = np.array([[bool(int(char)) for char in list(line)] for line in puzzle_input.splitlines()])
N_Lines, N_Char_Per_Line = Field.shape

# %% Part 1
route = np.array([(((3 * n_line) % N_Char_Per_Line), n_line) for n_line in range(N_Lines)])
print(np.count_nonzero(Field[route[:, 1], route[:, 0]]))

# %% Part 2

n_tree = 1
for x, y in [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]:
    route = np.array([(((x * n_line) % N_Char_Per_Line), y * n_line) for n_line in range(N_Lines)])
    route = route[:int(N_Lines/y)][:]
    n_tree *= np.count_nonzero(Field[route[:, 1], route[:, 0]])
print(f"Answer is {n_tree}")
