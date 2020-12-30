# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 10:53:26 2020

@author: kbasa
"""

from pathlib import Path
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 220


def read_input():
    """Make a dictionary of tiles."""
    tiles_raw = {}
    P_IN = Path.cwd().joinpath("input.txt").read_text()
    tiles_str = P_IN.strip("Tile ").split("\n\nTile ")

    for tile_str in tiles_str:
        no, content = tile_str.split(":\n")
        no = int(no)
        tiles_raw[no] = content
    return tiles_raw


@dataclass
class Tile:
    no: int
    input_text: str

    def __post_init__(self):
        text = self.input_text.replace("#", "1").replace(".", "0")
        array = [[int(j) for j in row] for row in text.splitlines()]
        self.image_orig = np.array(array, dtype="bool")
        self.orientation = "orig"
        self.generate_possible_images()

    def generate_possible_images(self):
        pos_imgs = dict()
        pos_imgs["orig"] = self.image_orig
        pos_imgs["rot90"] = np.rot90(self.image_orig)
        pos_imgs["rot180"] = np.rot90(pos_imgs["rot90"])
        pos_imgs["rot270"] = np.rot90(pos_imgs["rot180"])
        pos_imgs["flipLR"] = np.fliplr(self.image_orig)
        pos_imgs["flipUD"] = np.flipud(self.image_orig)
        pos_imgs["rot90flipUD"] = np.flipud(pos_imgs["rot90"])
        pos_imgs["rot90flipLR"] = np.fliplr(pos_imgs["rot90"])
        self.pos_imgs = pos_imgs

    def image(self):
        return self.pos_imgs[self.orientation]

    def right(self):
        return self.image()[:, 9]

    def left(self):
        return self.image()[:, 0]

    def top(self):
        return self.image()[0, :]

    def bottom(self):
        return self.image()[9, :]


def create_tiles_dictionary():
    global tiles
    tiles = {"placed": [], "not_placed": []}
    for key, val in read_input().items():
        tiles["not_placed"].append(Tile(key, val))


def reset_frame_extent():
    """Make a list that stores the minimum and maximum coordinates the placed tile
    pieces have spread upon.

    [row_min, row_max, column_min, column_max]
    """
    global frame_extent
    frame_extent = list(origin) + list(origin)


def check_if_pos_within_frame_extent(pos):
    """Check if the puzzle pieces placed on the canvas are not
    spread out wider or higher than intended edge_size."""
    global frame_extent
    i, j = pos
    if (frame_extent[1] - i < edge_size) and (i - frame_extent[0] < edge_size)\
        and (frame_extent[3] - j < edge_size) and (j - frame_extent[2] < edge_size):
        return True
    else:
        return False


def update_frame_extent(pos):
    global frame_extent
    i, j = pos
    frame_extent[0] = min(frame_extent[0], i)
    frame_extent[1] = max(frame_extent[1], i)
    frame_extent[2] = min(frame_extent[2], j)
    frame_extent[3] = max(frame_extent[3], j)


def place_a_tile(tile, pos):
    global canvas, tiles
    i, j = pos
    canvas[i][j] = tile
    update_frame_extent(pos)
    tiles["placed"].append(tile)


def check_if_tile_is_a_fit(tile, pos):
    global canvas
    i, j = pos
    above_tile = canvas[i-1][j] if (i > 0) else None
    below_tile = canvas[i+1][j] if (i < len(canvas) - 1) else None
    right_tile = canvas[i][j+1] if (j < len(canvas) - 1) else None
    left_tile = canvas[i][j-1] if (j > 0) else None
    if canvas[i][j] is not None:
        return False
    if all([neighbor is None for neighbor in [above_tile, below_tile, right_tile, left_tile]]):
        return False  # not neighboring any other tile
    if above_tile:
        if not all(above_tile.bottom() == tile.top()):
            return False
    if below_tile:
        if not all(below_tile.top() == tile.bottom()):
            return False
    if right_tile:
        if not all(right_tile.left() == tile.right()):
            return False
    if left_tile:
        if not all(left_tile.right() == tile.left()):
            return False
    return True


# %% Main loop part 1
create_tiles_dictionary()
edge_size = int(len(tiles["not_placed"])**0.5)
canvas = [[None] * (edge_size * 2 - 1) for _ in range((edge_size * 2 - 1))]
origin = (int(edge_size - 1), int(edge_size - 1))
reset_frame_extent()
orientation_keys = list(tiles["not_placed"][0].pos_imgs.keys())

count = 0
tile = tiles["not_placed"].pop()
place_a_tile(tile, origin)


while len(tiles["not_placed"]) > 0:
    count += 1
    print(f"Relooping: {count}")

    for i in range(len(canvas)):
        for j in range(len(canvas)):
            pos = (i, j)
            if check_if_pos_within_frame_extent(pos):
                for tile in tiles["not_placed"]:
                    for orientation in orientation_keys:
                        tile.orientation = orientation
                        if check_if_tile_is_a_fit(tile, pos):
                            place_a_tile(tile, pos)
                            tiles["not_placed"].remove(tile)
                            break

corner_tiles = [canvas[frame_extent[0]][frame_extent[2]],
                canvas[frame_extent[0]][frame_extent[3]],
                canvas[frame_extent[1]][frame_extent[2]],
                canvas[frame_extent[1]][frame_extent[3]]]

corner_tile_ID_prod = np.prod([tile.no for tile in corner_tiles], dtype="int64")
print(f"Product of corner nos: {corner_tile_ID_prod}")


# %% Part 2
image_edge_length = edge_size * 8
image = np.empty((image_edge_length, image_edge_length), dtype="bool")
for i in range(edge_size):
    for j in range(edge_size):
        tile = canvas[frame_extent[0] + i][frame_extent[2] + j]
        i_start, j_start = i*8, j*8
        image[i_start:i_start+8, j_start:j_start+8] = tile.image()[1:9, 1:9]


def check_pos_for_monster(image_to_check, pos):
    i, j = pos
    edge_length = image_to_check.shape[0]
    if i > (edge_length - 3) or j > (edge_length - 20):
        return False

    l1 = image_to_check[i, j:j+20]
    l2 = image_to_check[i+1, j:j+20]
    l3 = image_to_check[i+2, j:j+20]

    if l1[[18]] and all(l2[[0, 5, 6, 11, 12, 17, 18, 19]])\
       and all(l3[[1, 4, 7, 10, 13, 16]]):
        return True
    else:
        return False


def count_monsters(image_to_check):
    edge_length = image_to_check.shape[0]
    monster_count = 0
    for i in range(edge_length):
        for j in range(edge_length):
            if check_pos_for_monster(image_to_check, (i, j)):
                print(f"Monster at {i, j}")
                monster_count += 1
    return monster_count


# %% Create a list with each possible orientation of the image (8 in total)
images = []
images.append(image)
images.append(np.rot90(image))
images.append(np.rot90(np.rot90(image)))
images.append(np.rot90(np.rot90(np.rot90(image))))
images.append(np.fliplr(image))
images.append(np.flipud(image))
images.append(np.flipud(np.rot90(image)))
images.append(np.fliplr(np.rot90(image)))

print()
for image in images:
    n_monster = count_monsters(image)
    if n_monster > 0:
        print(f"{n_monster} monsters found.")
        print(f"Total number of '#': {np.sum(image)}")
        print(f"Roughness: {np.sum(image) - n_monster * 15}")
        image_to_show = image

plt.imshow(image_to_show)
