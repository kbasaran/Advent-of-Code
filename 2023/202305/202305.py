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
        row_data = [seeds[i*2], seeds[i*2] + seeds[i*2+1] - 1, 0]
        df.loc[len(df)] = add_destination_values(row_data)
    return df

df = build_start_vector(seeds)

for map_definition in maps:
    # print("\n\n-------------New map---------------")
    # print(df)
    df = df.sort_values(by="source_start")
    df_next = pd.DataFrame(columns=df.columns)
    for index, old_row in df.iterrows():
        row = pd.DataFrame(columns=df.columns)
        row.loc[0] = old_row.copy()
        # print("---------New line--------")
        # print(old_row)
        # print()

        while len(row) > 0:
            starting_rows = len(row)
            print(row.index)
            i = row.index[0]
            row_source_start, row_source_end, row_diff, row_dest_start, row_dest_end = row.loc[i]
            # changed = False

            overlapped=False
            for map_source_start, map_source_end, map_diff in sorted(map_definition.source_destination_diff, key=lambda x: x[0]+x[2]):
                # print("Map data: ", map_source_start, map_source_end, map_diff)

                if (map_source_end > row_dest_start) & (map_source_start < row_dest_end):
                    overlapped=True
                    # these are all the rows where the existing vector in df has some overlap with the new vector definition in map
                    # move them to new dataframe

                    # add the section with full overlap of existing vector and new vector definition
                    start = max(row_dest_start, map_source_start) - row_diff
                    end = min(row_dest_end, map_source_end) - row_diff
                    overlap = [start, end, row_diff + map_diff]
                    df_next.loc[len(df_next)] = add_destination_values(overlap)  # replace old row

                    # add the section where existing vector starts earlier and needs to project the first section with no diff
                    if row_dest_start < map_source_start:
                        start = row_dest_start - row_diff
                        end = map_source_start - row_diff
                        lower_section = [start, end, row_diff]
                        row.loc[max(row.index)+1] = add_destination_values(lower_section)

                    # add the section where existing vector ends later and needs to project that remaining section with no diff
                    if row_dest_end > map_source_end:
                        start = map_source_end - row_diff
                        end = row_dest_end - row_diff
                        upper_section = [start, end, row_diff]
                        row.loc[max(row.index)+1] = add_destination_values(upper_section)

                    row = row.drop(i)
                    break

            if not overlapped:
                df_next = pd.concat([df_next, row])
                break

            # print(df)
            # print(df_next)
            # print()


    df = df_next


print("\n\nResult:")
print(df.sort_values(by="dest_start"))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
