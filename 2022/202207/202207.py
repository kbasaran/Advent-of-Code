# 2022 Day 07

# Receive input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from anytree import NodeMixin, RenderTree

start_time = perf_counter()

class folder(NodeMixin):
    def __init__(self, name, files=None, parent=None, children=None):
        super(folder, self).__init__()
        self.name = name

        self.files = {}
        if files:
            self.add_files(files)

        self.parent = parent

        if children:
            self.children = children

    def add_files(self, files: list):
        for file_name, size in files:
            assert isinstance(file_name, str)
            assert isinstance(size, int)
            self.files[file_name] = size

    def get_files(self):
        return self.files


root = folder(name="/")
nodes = []
nodes.append(folder(name="man", parent=root))
nodes[0].add_files([("a", 10), ("b", 20)])
print([children.get_files().values() for children in root.children])


# how to access the folder instance based on the path name given by the another instance



print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
