# 2023 Day 03

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from functools import lru_cache
from itertools import product
import numpy as np

start_time = perf_counter()

# ---- Part 1

def make_into_array(p_in, dtype):
    array = [list(line) for line in p_in.strip().split("\n")]
    return np.array(array, dtype=dtype)

# Global
schematic = make_into_array(p_in, str)

@lru_cache
def get_relative_adjacent_coords_to_point(max_dist) -> list:
    # returns list of relative adjacent coordinates, each being a 2-tuple
    relative_coords = set(product(range(-max_dist, max_dist+1), repeat=2))
    relative_coords.discard((0, 0))
    return relative_coords

@lru_cache
def coord_is_valid(coord):
    global schematic
    if coord[0] >= schematic.shape[0] or coord[0] < 0:
        return False
    if coord[1] >= schematic.shape[1] or coord[1] < 0:
        return False
    return True

def get_adjacent_coords_to_point(xy: tuple) -> list:
    # returns list of adjacent coordinates, each being a 2-tuple
    coords = [(xy[0] + x_offset, xy[1] + y_offset) for (x_offset, y_offset) in get_relative_adjacent_coords_to_point(1)]
    return [coord for coord in coords if coord_is_valid(coord)]

def get_adjacent_coords_to_line(coords: tuple) -> list:
    # returns list of adjacent coordinates, each being a 2-tuple
    adjacent_coords = set()
    for xy in coords:
        adjacent_coords.update(get_adjacent_coords_to_point(xy))
    for xy in coords:
        adjacent_coords.add(xy)
        adjacent_coords.remove(xy)
    return adjacent_coords

def find_star_symbol_coordinates():
    global schematic
    gear_locs = np.where(schematic == "*")
    return tuple(zip(*gear_locs))

def has_common_element(t1: tuple, t2: tuple):
    for val in t1:
        if val in t2:
            return True
    return False

def find_part_numbers():
    global schematic
    # returns coordinates and value of part numbers
    found_numbers = {}  # keys are coords, vals are the numbers
    in_number = False
    row_width = len(p_in.split("\n")[0])
    digits = {}
    for i, char in enumerate(schematic.flatten()):  # iterate over characters in string
        if not in_number and char.isdigit():  # start of a number
            in_number = True
            digits[i] = char
        elif in_number and char.isdigit():  # inside a number
            digits[i] = char
        elif in_number and not char.isdigit():  # end of a number
            number = int("".join([str(digit) for digit in digits.values()]))

            # add each coordinate of the number to a set
            coords = list()
            for xy_flattened, char in digits.items():
                x, y = divmod(xy_flattened, row_width)
                coords.append((x, y))
                
            # add to the set as a new number
            found_numbers[tuple(coords)] = number
            
            # reset variables
            digits.clear()
            coords.clear()
            in_number = False
        else:
            continue

    return found_numbers

star_symbol_coords = find_star_symbol_coordinates()
found_numbers = find_part_numbers()
valid_pns = [number for coords, number in found_numbers.items() if has_common_element(star_symbol_coords, get_adjacent_coords_to_line(coords))]
print(sum(valid_pns))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2

def find_adjacent_numbers_to_point(coord):
    adjacent_coords = get_adjacent_coords_to_point(coord)
    adjacent_numbers = {}
    for coord in adjacent_coords:
        for number_coords, number in found_numbers.items():
            if coord in number_coords:
                adjacent_numbers[number_coords] = number
                continue
    return adjacent_numbers

def find_gears():
    gears = []
    for star_coord in star_symbol_coords:
        adjacent_numbers = find_adjacent_numbers_to_point(star_coord)
        if len(adjacent_numbers) == 2:
            vals = list(adjacent_numbers.values())
            gears.append(vals[0] * vals[1])
    return gears

print(sum(find_gears()))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
