# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from itertools import product

start_time = perf_counter()


def parse_input(p_in):
    start_str, rule_str = p_in.split("\n\n")
    rules = {text[0]: text[1] for text in [row_text.split(" -> ") for row_text in rule_str.splitlines()]}
    start_keys = [start_str[i:i+2] for i in range(len(start_str) - 1)]
    return start_keys, rules


def make_trans_matrix(p_in):
    start_keys, rules = parse_input(p_in)
    all_letters = set("".join([*rules.keys(), *rules.values()]))
    combos = ["".join(combo) for combo in product(all_letters, repeat=2)]
    trans_dict = dict.fromkeys(combos)

    for key, val in rules.items():
        new_keys = key[0] + rules[key], rules[key] + key[1]
        trans_dict[key] = new_keys

    return combos, all_letters, trans_dict, start_keys


def count_total_letters(appearance_count_all_steps, all_letters, start_keys):
    letter_appearance = dict.fromkeys(all_letters, 0)
    for combo, occurrence in appearance_count_all_steps.items():
        for letter in combo:
            letter_appearance[letter] += occurrence
    # first and last values of string appear only in one combo, all else appears in two combos
    letter_appearance[start_keys[0][0]] += 1
    letter_appearance[start_keys[-1][-1]] += 1
    return {letter: int(val / 2) for letter, val in letter_appearance.items()}


def solve_steps(p_in):
    combos, all_letters, trans_dict, start_keys = make_trans_matrix(p_in)
    appearance_count_all_steps = dict.fromkeys(combos, 0)
    for key in start_keys:
        appearance_count_all_steps[key] += 1

    for step in range(40):
        appearance_count = dict.fromkeys(combos, 0)
        for key, val in appearance_count_all_steps.items():
            for key2 in trans_dict[key]:
                appearance_count[key2] += val
        appearance_count_all_steps = appearance_count
    letter_appearances = count_total_letters(appearance_count_all_steps, all_letters, start_keys)
    print(f"\nAnswer: {max(letter_appearances.values()) - min(letter_appearances.values())}")


solve_steps(p_in)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
