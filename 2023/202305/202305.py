# 2023 Day 05

# Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
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
        self.source_destination_diff = []
        for line in map_string.strip().split("\n")[1:]:
            p1, p2, p3 = [int(val) for val in line.split()]
            self.source_destination_diff.append(((p2, p2+p3, p1-p2)))
            # tuple of source_start, source_end, from source to destination difference (dest - source)

def get_maps(p_in):
    maps = []
    for map_string in p_in.strip().split("\n\n")[1:]:
        maps.append(Map(map_string))
    return maps


def get_columns(maps):
    columns = set()
    for map_definition in maps:
        columns.add(map_definition.source)
        columns.add(map_definition.destination)
    return list(columns)

def create_df(seeds, maps):
    df = pd.DataFrame(columns=get_columns(maps), dtype=int)
    df["seed"] = seeds
    return df

def process_maps(df, maps):
    for map_definition in maps:
        df[map_definition.destination] = df[map_definition.source]
        for source_start, source_end, diff in map_definition.source_destination_diff:
            df.loc[(df[map_definition.source] >= source_start) & (df[map_definition.source] < source_end), map_definition.destination] += diff
    return df

seeds = get_seeds(p_in)
maps = get_maps(p_in)
df = create_df(seeds, maps)
print(process_maps(df, maps)["location"].min())
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2

def add_destination_values(_map: list) -> list:
    return [*_map, _map[0] + _map[2], _map[1] + _map[2]]

def build_start_vector(seeds):
    columns = ["source_start", "source_end", "diff", "dest_start", "dest_end"]
    df = pd.DataFrame(columns=columns, dtype=int)
    for i in range(len(seeds) // 2):
        row_data = [seeds[i], seeds[i] + seeds[i+1], 0]
        df.loc[len(df)] = add_destination_values(row_data)
    return df

df = build_start_vector(seeds)
print(df)
for map_definition in maps:
    df = df.sort_values(by="source_start")
    for source_start, source_end, diff in map_definition.source_destination_diff:
        for i in df.index:
            if source_start == 77 and i == 7:
                pass
            old_row = df.loc[i, :].copy()  # take a copy of row to temp. variable
            # df.drop(i, inplace=True) # remove the row from df
            if (source_end > old_row["dest_start"]) & (source_start < old_row["dest_end"]):
                # these are all the rows where the existing vector in df has some overlap with the new vector definition in map
                
                # add the section with full overlap of existing vector and new vector definition
                overlap = [max(old_row["dest_start"], source_start), min(old_row["dest_end"], source_end), diff]
                df.loc[i] = add_destination_values(overlap)  # replace old row
                
                # add the section where existing vector starts earlier and needs to project the first section with no diff
                if old_row["dest_start"] < source_start:
                    lower_section = [old_row["dest_start"], source_start, 0]
                    df.loc[len(df)] = add_destination_values(lower_section)
                
                # add the section where existing vector ends later and needs to project that remaining section with no diff
                if old_row["dest_end"] > source_end:
                    upper_section = [source_end, old_row["dest_end"], 0]
                    df.loc[len(df)] = add_destination_values(upper_section)
                

                
            else:
                # just move over the range as it is
                same_section = [old_row["dest_start"], old_row["dest_end"], 0]
                df.loc[i] = add_destination_values(same_section)  # replace old row

        print("\n\n")
        print(source_start, source_end, diff)
        print(df)


print("\n\nResult:")
print(df.sort_values(by="dest_start"))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
