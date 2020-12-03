# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:21:41 2020

@author: kerem.basaran
"""

import pyperclip

def required_paper(present_dims):
    vals = [float(dim) for dim in present_dims.split("x")]
    min_d, mid_d, max_d = sorted(vals)
    return 2 * ((min_d * mid_d) + (mid_d * max_d) + (min_d * max_d)) + min_d * mid_d

def required_ribbon(present_dims):
    vals = [float(dim) for dim in present_dims.split("x")]
    min_d, mid_d, max_d = sorted(vals)
    return 2 * (min_d + mid_d) + (min_d * mid_d * max_d)

puzzle_input = pyperclip.paste()

tot_required_paper = 0
tot_required_ribbon = 0
for present_dims in puzzle_input.splitlines():
    if "x" in present_dims:
        tot_required_paper += required_paper(present_dims)
        tot_required_ribbon += required_ribbon(present_dims)
    else:
        print(f"Skipping line: {present_dims}")

print(f"Required paper: {tot_required_paper}")
print(f"Required ribbon: {tot_required_ribbon}")
