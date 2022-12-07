# 2022 Day 07

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from anytree import Node, RenderTree
import numpy as np

start_time = perf_counter()


def create_tree(p_in):
    root = Node(name="root")
    cwd = root
    for line in p_in.splitlines():
        parts = line.split()

        # ls listing. create files and folders here.
        if "".join(parts[:2]) == "$ls":
            ls_listing = True
            continue
        elif parts[0] == "$":
            ls_listing = False

        if ls_listing:
            if parts[0] == "dir":
                new_child = Node(name=parts[1], parent=cwd)
                # this will give an error if same folder is ls'd twice
                new_child.files = {}
            else:
                cwd.files[parts[1]] = int(parts[0])

        # change directory
        elif "".join(parts[:2]) == "$cd":
            cd_dir = parts[2]

            if cd_dir == "/":
                cwd = root
                root.files = {}

            elif cd_dir == "..":
                cwd = cwd.parent

            else:
                for child in cwd.children:
                    if child.name == cd_dir:
                        cwd = child
                if cwd.name != cd_dir:
                    raise ValueError(f"cd to {cd_dir} failed", cwd)

        else:
            raise ValueError(f"Don't know what to do with this line: {line}")
    return root


def find_total_size(folder):
    return sum([sum(node.files.values()) for node in (*folder.descendants, folder)])


if __name__ == "__main__":
    root = create_tree(p_in)
    # print(RenderTree(root))
    dir_sizes = np.array([find_total_size(folder) for folder in (root, *root.descendants)])

    print(sum(dir_sizes[dir_sizes < 100_000]))  # Part 1

    cur_free_space = 70_000_000 - find_total_size(root)
    print(min(dir_sizes[dir_sizes >= (30_000_000 - cur_free_space)]))  # Part 2


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
