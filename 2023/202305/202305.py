# 2023 Day 05

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import pandas as pd

start_time = perf_counter()

# ---- Part 1

def get_seeds(p_in):
    cropped = p_in.strip().removeprefix("seeds: ").partition("\n")[0]
    return [int(val) for val in cropped.split()]

class Map:
    def __init__(self, map_string):
        self.source, self.destination = map_string.strip().split()[0].split("-to-")
        self.source_destination_pairs = []
        for line in map_string.strip().split("\n")[1:]:
            p1, p2, p3 = [int(val) for val in line.split()]
            self.source_destination_pairs.append(((p2, p2+p3, p1-p2)))
            # tuple of source_start, source_end, from source to destination difference (dest - source)

def get_maps(p_in):
    maps = []
    for map_string in p_in.strip().split("\n\n")[1:]:
        maps.append(Map(map_string))
    return maps

seeds = get_seeds(p_in)
maps = get_maps(p_in)

columns = set()
for map_object in maps:
    columns.add(map_object.source)
    columns.add(map_object.destination)

df = pd.DataFrame(columns=list(columns), dtype=int)
df["seed"] = seeds

for map_object in maps:
    df[map_object.destination] = df[map_object.source]
    # df = df.sort_values(by=map_object.destination)
    for source_start, source_end, diff in map_object.source_destination_pairs:
        df.loc[(df[map_object.source] >= source_start) & (df[map_object.source] < source_end), map_object.destination] += diff

df_initial_seeds = df[df["seed"].isin(seeds)]
print(df_initial_seeds["location"].min())
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
