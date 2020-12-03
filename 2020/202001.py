# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:44:16 2020

@author: kerem.basaran
"""

import numpy as np
import pyperclip

# puzzle_input = pyperclip.paste().splitlines()
target_val = 2020

# %% Part 1
exp_report = np.array(puzzle_input, dtype=np.int32)
sum_matrix_2d = np.tril([exp_report + val for val in exp_report], -1)

chosen_entries = [exp_report[i].item() for i in np.where(sum_matrix_2d == target_val)]

print(chosen_entries, np.product(chosen_entries))


# %% Part 2
exp_report = np.array(puzzle_input, dtype=np.int32)
sum_matrix_3d = np.tril([sum_matrix_2d + val for val in exp_report], -1)

chosen_entries = [exp_report[i] for i in np.where(sum_matrix_3d == target_val)]

print(chosen_entries, np.product(chosen_entries))
