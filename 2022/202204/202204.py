# 2022 Day 04

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from dataclasses import dataclass

start_time = perf_counter()


@dataclass
class Area:
    min1: int
    max1: int
    min2: int
    max2: int

    def fully_overlapping(self):
        if self.min1 <= self.min2 and self.max1 >= self.max2 or\
            self.min2 <= self.min1 and self.max2 >= self.max1:
                return True

    def at_least_one_overlap(self):
        if self.max1 >= self.min2 and self.max1 <= self.max2 or\
            self.max2 >= self.min1 and self.max2 <= self.max1:
                return True


def parse_line(area_text):
    area_1_text, area_2_text = area_text.split(",")
    min1, max1 = [int(val) for val in area_1_text.split("-")]
    min2, max2 = [int(val) for val in area_2_text.split("-")]
    return min1, max1, min2, max2


if __name__ == "__main__":
    areas = []
    for area_text in p_in.splitlines():
        area = Area(*parse_line(area_text))
        areas.append(area)
    
    print([area.fully_overlapping() for area in areas].count(True))  # Part 1
    print([area.at_least_one_overlap() for area in areas].count(True))  # Part 2
    
    
    print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
