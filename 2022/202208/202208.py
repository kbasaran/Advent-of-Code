# 2022 Day 08

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 150

start_time = perf_counter()


def parse_input(p_in):
    rows = []

    for row in p_in.splitlines():
        rows.append([int(val) for val in row])
    heights = np.array(rows,
                      dtype=np.intp,
                      )
    return heights

def in_line_of_sight(trees: list) -> set:
    "Returns index of visible trees in given list of tree heights - looks from one side"
    to_check_mask = np.full(len(trees), True)
    # np.full returns an array where all values are positional argument 2. dtype is inferred.
    visibles = set()

    while any(to_check_mask):
        trees_to_check = np.array(trees) * to_check_mask
        i_highest = int(np.flatnonzero(trees_to_check == max(trees_to_check))[0])  
        visibles.add(i_highest)
        to_check_mask[i_highest:] = False

    return visibles

def visible_either_side(trees: list) -> set:
    "Returns index of visible trees in given list of tree heights - looks from two sides"
    visibles = set()
    visibles.update(in_line_of_sight(trees))
    visibles.update([len(trees) -1 - val for val in in_line_of_sight(trees[::-1])])
    return visibles

def coords_of_line_of_sight(i_visibles: list, row: int=None, col: int=None) -> list:
    assert None in (row, col)

    if row is not None:
        return [(row, i) for i in i_visibles]
    elif col is not None:
        return [(i, col) for i in i_visibles]
    else:
        raise ValueError("define row or col!")

def look_from_all_sides(p_in: str) -> (np.array, set):
    "Scan the matrix 'height_map' for visibility on all sides."
    height_map = parse_input(p_in)
    coords_of_visible_trees = set()
    
    for i_row in range(height_map.shape[0]):
        i_visibles = visible_either_side(height_map[i_row, :])
        coords_of_visible_trees.update(coords_of_line_of_sight(i_visibles, row=i_row))

    for i_col in range(height_map.shape[1]):
        i_visibles = visible_either_side(height_map[:, i_col])
        coords_of_visible_trees.update(coords_of_line_of_sight(i_visibles, col=i_col))

    return height_map, coords_of_visible_trees

def visible_from_tree_house(height_map: np.array, coord: tuple) -> dict:
    row, col = coord
    trees_on_direction = dict.fromkeys(list("udlr"), np.array([]))
    n_visible_per_direction = dict.fromkeys(list("udlr"))
    trees_on_direction["r"] = height_map[row, col+1:]
    trees_on_direction["l"] = np.flip(height_map[row, :col])
    trees_on_direction["u"] = np.flip(height_map[:row, col])
    trees_on_direction["d"] = height_map[row+1:, col]

    for key, trees in trees_on_direction.items():
        i_same_or_taller = np.flatnonzero(trees >= height_map[coord])
        # flatnonzero returns indices of nonzero elements (in this case True's) after flattening the array
        if len(i_same_or_taller) > 0:
            n_visible = int(i_same_or_taller[0]) + 1
        else:
            n_visible = len(trees)
        n_visible_per_direction[key] = n_visible

    return n_visible_per_direction

if __name__ == "__main__":
    height_map, visibles = look_from_all_sides(p_in)
    print(len(visibles))  # Part 1
    
    max_scenic = 0
    for coord in [(row, col) for row in range(height_map.shape[0]) for col in range(height_map.shape[1])]:
        n_visible_list = list(visible_from_tree_house(height_map, coord).values())
        max_scenic = max(max_scenic, np.product(n_visible_list))

    print(max_scenic)  # Part 2


    print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")

    plt.matshow(height_map)
    plt.title("202208")