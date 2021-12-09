# %% Take input
# with open('input.txt') as f:
with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import pandas as pd

start_time = perf_counter()


class Display():

    number_codes = {0: "abcefg",
                    1: "cf",
                    2: "acdeg",
                    3: "acdfg",
                    4: "bcdf",
                    5: "abdfg",
                    6: "abdefg",
                    7: "acf",
                    8: "abcdefg",
                    9: "abcdfg",
                    }

    letters = [val for val in "abcdefg"]
    numbers = list(range(10))

    def __init__(self):
        self.table = pd.DataFrame(index=self.letters,
                                  columns=self.letters,
                                  dtype=str,
                                  )
        self.len_of_number = {number: len(self.number_codes[number]) for number in self.number_codes.keys()}
        self.display_combos = []

    def add_combo(self, combo):
        length = len(combo)
        numbers_with_same_length = [number for number in self.number_codes.keys() if len(self.number_codes[number]) == length]
        segments_of_these_numbers = sorted(set("".join([self.number_codes[number] for number in numbers_with_same_length])))
        segments_not_used_by_these_numbers = set([val for val in self.letters if val not in segments_of_these_numbers])

        sorted_combo = "".join(sorted(combo))
        self.display_combos.append(sorted_combo)

    def add_combos(self, combos):
        for combo in combos:
            self.add_combo(combo)

    def count_1478(self):
        counter = 0
        for combo in self.display_combos:
            if list(self.len_of_number.values()).count(len(combo)) == 1:
                counter += 1
        return counter

def test():
    pattern = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    display = Display()
    display.add_combos(pattern.split()[:10])

test()

def part_1(p_in):
    counter_1478 = 0
    for row_text in p_in.split("\n"):
        display_combos = row_text.split()[-4:]
        display = Display()
        display.add_display_combos(display_combos)
        counter_1478 += display.count_1478()
    print(f"\n--Part 1--\nAnswer: {counter_1478}")


# part_1(p_in)



print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
