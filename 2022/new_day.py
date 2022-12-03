# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:19:23 2022

@author: kerem.basaran
"""

import os
import datetime
import argparse

parser = argparse.ArgumentParser(description='Start a new AoC day')
parser.add_argument('day',
                    metavar="d",
                    nargs="?",
                    type=int,
                    default=datetime.datetime.today().day,
                    choices=range(1, 32),
                    )
args = parser.parse_args()


def check_if_in_a_year_folder():
    base_folder = os.path.basename(os.getcwd())
    try:  # could be: year.isdiecimal() and 2010 < year < 2099
        year = int(base_folder)
        if 2010 < year < 2099:
            return True
        else:
            raise ValueError
    except (ValueError, NameError):
        return False


def make_folder(day):
    cwd = os.getcwd()
    year = int(os.path.basename(cwd))
    folder_name = str(year) + str(day).zfill(2)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    file_name = folder_name + ".py"
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(f"# {year} Day {str(day).zfill(2)}"
"""\n\n# Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

# Code here



print(f"\\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
"""
                    )
            print(f"Created file: {file_name}")

        for input_file in ("input.txt", "test.txt"):
            file_path = os.path.join(folder_name, input_file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    print(f"Created file: {input_file}")


def create_new_day_folder(day):
    assert check_if_in_a_year_folder(), ("Current working folder is not a year it seems: "
                                         f"'./{os.path.basename(os.getcwd())}'"
                                         )
    make_folder(day)


if __name__ == "__main__":
    create_new_day_folder(args.day)
