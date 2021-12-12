# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
# with open("test2.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

# Code here


conns = {}
nodes = set()
for row in p_in.splitlines():
    n1, n2 = row.split("-")
    for key, val in [[n1, n2], [n2, n1]]:
        if key not in conns.keys():
            conns[key] = set()
        conns[key].add(val)


def search_paths(paths, path):
    for conn in conns[path[-1]]:
        if conn.isupper() or conn not in path:
            if conn == "end":
                paths.append([*path, "end"])
            else:
                search_paths(paths, [*path, conn])


def part_1():
    paths = []
    search_paths(paths, ["start"])
    print(f"\n--Part 1--\nAnswer: {len(paths)}")


part_1()

# print(f"\n--Part 2--\nAnswer: {var2}")
print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
