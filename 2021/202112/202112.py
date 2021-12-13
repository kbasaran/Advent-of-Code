# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
# with open("test2.txt") as f:
    p_in = f.read()

from time import perf_counter
from copy import deepcopy

start_time = perf_counter()


def parse_input(p_in):
    global conns
    conns = {}
    for row in p_in.splitlines():
        n1, n2 = row.split("-")
        for key, val in [[n1, n2], [n2, n1]]:
            if key not in conns.keys():
                conns[key] = set()
            conns[key].add(val)


def search_paths_p1(paths, path):
    global conns
    for conn in conns[path[-1]]:
        if conn.isupper() or conn not in path:
            if conn == "end":
                paths.append([*path, "end"])
            else:
                search_paths_p1(paths, [*path, conn])


def part_1():
    paths = []
    search_paths_p1(paths, ["start"])
    print(f"\n--Part 1--\nAnswer: {len(paths)}")


class Path_p2():
    def __init__(self, path):
        self.path = path
        self.twice_visited = None

    def last_element(self):
        return self.path[-1]

    def try_add_conn(self, conn):
        if conn.isupper():
            self.path.append(conn)
            return True
        elif conn in self.path:
            if conn == self.twice_visited:
                return None
            elif not self.twice_visited and conn not in ["start", "end"]:
                self.twice_visited = conn
                self.path.append(conn)
                return True
            else:
                # conn exists and we already visited another lowercase node twice
                return None
        else:
            self.path.append(conn)
            return True


def search_paths_p2(paths, path):
    global conns
    for conn in conns[path.last_element()]:
        new_path = deepcopy(path)
        if new_path.try_add_conn(conn):
            if new_path.last_element() == "end":
                paths.append(new_path)
            else:
                search_paths_p2(paths, new_path)


def part_2():
    paths = []
    search_paths_p2(paths, Path_p2(["start"]))
    print(f"\n--Part 2--\nAnswer: {len(paths)}")


parse_input(p_in)
part_1()
part_2()

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
