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
    for map_section in maps:
        columns.add(map_section.source)
        columns.add(map_section.destination)
    return list(columns)

def create_df(seeds, maps):
    df = pd.DataFrame(columns=get_columns(maps), dtype=int)
    df["seed"] = seeds
    return df

def process_maps(df, maps):
    for map_section in maps:
        df[map_section.destination] = df[map_section.source]
        for source_start, source_end, diff in map_section.source_destination_diff:
            df.loc[(df[map_section.source] >= source_start) & (df[map_section.source] < source_end), map_section.destination] += diff
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

for map_section in maps:
    # print("\n\n-------------New map---------------")
    # print(df)
    df_next = pd.DataFrame(columns=df.columns)
    for index, vector in df.iterrows():
        vector_segments = pd.DataFrame(columns=df.columns)
        vector_segments.loc[0] = vector.copy()
        # print("\n---------New line--------")
        # print(vector)
        # print()

        while len(vector_segments) > 0:
            i = vector_segments.index[0]
            row_source_start, row_source_end, row_diff, row_dest_start, row_dest_end = vector_segments.loc[i]

            overlapped=False
            for map_source_start, map_source_end, map_diff in map_section.source_destination_diff:
                
                if (map_source_end > row_dest_start) & (map_source_start < row_dest_end):
                    # existing vector has some overlap with the new vector definition in map
                    # move them to new dataframe
                    # print("Map data: ", map_source_start, map_source_end, map_diff)
                    overlapped=True

                    # add the section with full overlap of existing vector and new vector definition
                    start = max(row_dest_start, map_source_start) - row_diff
                    end = min(row_dest_end, map_source_end) - row_diff
                    overlap = [start, end, row_diff + map_diff]
                    df_next.loc[len(df_next)] = add_destination_values(overlap)
                    vector_segments = vector_segments.drop(i)

                    # add the section where existing vector starts earlier and needs to project the first section with no diff
                    if row_dest_start < map_source_start:
                        start = row_dest_start - row_diff
                        end = map_source_start - row_diff
                        lower_section = [start, end, row_diff]
                        lower_section_df = pd.DataFrame([add_destination_values(lower_section)], columns=vector_segments.columns)
                        vector_segments = pd.concat([vector_segments, lower_section_df], ignore_index=True)

                    # add the section where existing vector ends later and needs to project that remaining section with no diff
                    if row_dest_end > map_source_end:
                        start = map_source_end - row_diff
                        end = row_dest_end - row_diff
                        upper_section = [start, end, row_diff]
                        upper_section_df = pd.DataFrame([add_destination_values(upper_section)], columns=vector_segments.columns)
                        vector_segments = pd.concat([vector_segments, upper_section_df], ignore_index=True)

                    break

            if not overlapped:
                df_next = pd.concat([df_next, vector_segments])
                break

            # print(df)
            # print(df_next)
            # print()

    df = df_next

print("\n\nResult:")
print(df.sort_values(by="dest_start").iloc[0])
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
