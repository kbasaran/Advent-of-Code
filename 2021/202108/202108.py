# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import pandas as pd

start_time = perf_counter()


class Display():

    len_of_number = {0: 6,
                     1: 2,
                     2: 5,
                     3: 5,
                     4: 4,
                     5: 5,
                     6: 6,
                     7: 3,
                     8: 7,
                     9: 6,
                     }

    letters = [val for val in "abcdefg"]
    signal_outs = ["s-" + letter for letter in letters]
    display_segments = ["d-" + letter for letter in letters]
    numbers = list(range(10))

    def __init__(self):
        self.table = pd.DataFrame(index=[*self.display_segments, *self.signal_outs],
                                  columns=[*self.letters, *self.numbers],
                                  dtype=str,
                                  )
        self.display_combos = []

    def add_display_combo(self, combo):
        # check lengths
        for number in self.len_of_number.keys():
            if len(combo) == self.len_of_number[number]:
                letters_connected = ["d-" + letter for letter in combo]
                self.table[number].loc[letters_connected] = "X"
                if list(self.len_of_number.values()).count(len(combo)) == 1:
                    for letter in self.letters:
                        if letter not in combo:
                            self.table[number].loc["d-" + letter] = "."
        sorted_combo = "".join(sorted(combo))
        self.display_combos.append(sorted_combo)

    def add_display_combos(self, combos):
        for combo in combos:
            self.add_display_combo(combo)

    def count_1478(self):
        counter = 0
        for combo in self.display_combos:
            if list(self.len_of_number.values()).count(len(combo)) == 1:
                counter += 1
        return counter


def part_1(p_in):
    counter_1478 = 0
    for row_text in p_in.split("\n"):
        display_combos = row_text.split()[-4:]
        display = Display()
        display.add_display_combos(display_combos)
        counter_1478 += display.count_1478()
    print(f"\n--Part 1--\nAnswer: {counter_1478}")


part_1(p_in)



print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
