# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import pandas as pd
from itertools import permutations

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

    def __init__(self, combos_10, combos_4):
        self.table = pd.DataFrame(index=self.letters,
                                  columns=self.letters,
                                  dtype=bool,
                                  )
        # each column is a letter in the code
        # each row is the possible correct translation of them
        self.len_of_number = {number: len(self.number_codes[number]) for number in self.number_codes.keys()}
        self.combos_10 = []
        for combo in combos_10:
            sorted_combo = "".join(sorted(combo))
            self.combos_10.append(sorted_combo)
        self.process_combos_10()
        self.combos_4 = combos_4

    def process_combos_10(self):
        for combo in self.combos_10:
            # print(f"Adding combo: {combo}")
            length = len(combo)
            numbers_with_same_length = [number for number in self.number_codes.keys() if len(self.number_codes[number]) == length]
            segments_of_these_numbers = sorted(set("".join([self.number_codes[number] for number in numbers_with_same_length])))
            segments_not_used_by_these_numbers = set([val for val in self.letters if val not in segments_of_these_numbers])
            for letter in combo:
                self.table[letter][segments_not_used_by_these_numbers] = False

        # do translations with a dict. keys are combo values, values are actual segment that is aimed
        for permutation in permutations(self.letters, 7):
            # Check if it matches the lengths
            checks = []
            for i, coded_letter in enumerate(self.letters):
                checks.append(self.table[coded_letter][permutation[i]])
            if all(checks):
                # Check if it covers all 10 numbers
                checks2 = []
                translation_dict = dict(zip(self.letters, permutation))
                for combo in self.combos_10:
                    corrected_letters = "".join(sorted([translation_dict[letter] for letter in combo]))
                    checks2.append(corrected_letters in self.number_codes.values())
                if all(checks2):
                    self.translation_dict = translation_dict
                    break

    def decode_to_number(self, combo):
        corrected_letters = "".join(sorted([self.translation_dict[letter] for letter in combo]))
        numbers_matching = [number for number in self.number_codes.keys() if self.number_codes[number] == corrected_letters]
        if len(numbers_matching) == 1:
            return numbers_matching[0]
        else:
            return None

    def number_4_digit_display(self):
        digits = 0
        for i, combo in enumerate(self.combos_4):
            digits += self.decode_to_number(combo) * 10**(len(self.combos_4) - i - 1)
        return digits

    def count_1478(self):
        counter = 0
        number_code_lenghts = list(self.len_of_number.values())
        for combo in self.combos_4:
            if number_code_lenghts.count(len(combo)) == 1:
                counter += 1
        return counter


def parse_input(p_in):
    global displays
    displays = []
    for i, row_text in enumerate(p_in.split("\n")):
        combos_10 = row_text.split()[:10]
        combos_4 = row_text.split()[-4:]
        display = Display(combos_10, combos_4)
        if i % 20 == 19:
            print(f"Solved display {i + 1}")
        displays.append(display)


def part_1():
    global displays
    counter_1478 = 0
    for display in displays:
        counter_1478 += display.count_1478()
    print(f"\n--Part 1--\nAnswer: {counter_1478}")


def part_2():
    global displays
    sum_displays = 0
    for display in displays:
        sum_displays += display.number_4_digit_display()
    print(f"\n--Part 2--\nAnswer: {sum_displays}")


if __name__ == "__main__":
    parse_input(p_in)
    part_1()
    part_2()

    print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
