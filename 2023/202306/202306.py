# 2023 Day 06

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import polars as pl
from math import ceil, floor

start_time = perf_counter()

# ---- Part 1

def parse_input(p_in):
    line1 = p_in.strip().splitlines()[0]
    line2 = p_in.strip().splitlines()[1]
    times = [int(val) for val in line1.split()[1:]]
    distances = [int(val) for val in line2.split()[1:]]

    df = pl.DataFrame({"time": times, "distance": distances})

    return df

df = parse_input(p_in)

def get_roots(a, b, c):
    sqp = (b**2 - 4*a*c)**0.5
    return {"root_1": (-b + sqp)/2/a, "root_2": (-b - sqp)/2/a}

df = df.with_columns(pl.struct(["time", "distance"])
                      .map_elements(lambda x: get_roots(1, -x["time"], x["distance"]))
                      .alias("roots")
                      ).unnest("roots")
        
df = df.with_columns((pl.max_horizontal(["root_1", "root_2"]).ceil() - pl.min_horizontal(["root_1", "root_2"]).floor() - 1)
                     .cast(int)
                     .alias("possible press times")
                     )

print(sum(df.select("possible press times").product()))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2

time = int("".join([str(val) for val in df.select("time").to_series()]))
distance = int("".join([str(val) for val in df.select("distance").to_series()]))
roots = get_roots(1, -1 * time, distance).values()
sol_range = ceil(max(roots)) - floor(min(roots)) - 1

print(sol_range)
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")