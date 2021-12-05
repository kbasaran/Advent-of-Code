# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

start_time = perf_counter()


class Line():
    def __init__(self, start, end):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        self.xmin, self.xmax = min(self.x1, self.x2), max(self.x1, self.x2)
        self.ymin, self.ymax = min(self.y1, self.y2), max(self.y1, self.y2)
        self.straight = self._straight()

    def _straight(self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def diagonal_coords(self):
        points = set()

        x_points = np.arange(self.xmin, self.xmax + 1)
        if not self.xmin == self.x1:
            x_points = np.flip(x_points)

        y_points = np.arange(self.ymin, self.ymax + 1)
        if not self.ymin == self.y1:
            y_points = np.flip(y_points)

        for i in range(self.xmax - self.xmin + 1):
            points.add((x_points[i], y_points[i]))
        return points


def parse_input(p_in):
    global ocean_map, lines
    lines = set()
    xmax, ymax = 0, 0
    for row_str in p_in.splitlines():
        start, end = [[int(val) for val in part.split(",")]
                      for part in row_str.split(" -> ")]
        line = Line(start, end)
        lines.add(line)
        xmax = max(xmax, line.xmax)
        ymax = max(ymax, line.ymax)

    ocean_map = np.zeros([xmax + 1, ymax + 1], dtype=int)


def part_1():
    global ocean_map, lines
    for line in lines:
        if line.straight:
            ocean_map[line.xmin:line.xmax + 1,
                      line.ymin:line.ymax + 1] += 1
    print("\n--Part 1--"
          f"\nAnswer: {np.count_nonzero(ocean_map[ocean_map >= 2])}"
          )


def part_2():
    global ocean_map, lines
    for line in lines:
        if not line.straight:
            for point in line.diagonal_coords():
                ocean_map[point] += 1
    print("\n--Part 2--"
          f"\nAnswer: {np.count_nonzero(ocean_map[ocean_map >= 2])}"
          )


def visualize(ocean_map):
    plt.rcParams["figure.dpi"] = 300
    plt.imshow(np.transpose(ocean_map))


if __name__ == "__main__":
    parse_input(p_in)
    part_1()
    part_2()
    print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
    visualize(ocean_map)
