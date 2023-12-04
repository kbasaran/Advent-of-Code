# 2023 Day 04

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import numpy as np

start_time = perf_counter()

# ---- Part 1

def make_into_2darrays(p_in):
    winning = []
    scratched = []
    for line in p_in.strip().splitlines():
        line_cropped = line.split(": ")[1]
        left_hand, right_hand = line_cropped.split(" | ")
        winning.append(left_hand.split())
        scratched.append(right_hand.split())
    return np.array(winning, dtype=int), np.array(scratched, dtype=int)

winning, scratched = make_into_2darrays(p_in)

def count_matched_numbers_1d(element: list, test_element: list) -> int:
    return np.sum(np.isin(element, test_element))

count_matched_numbers_per_card = []
for i in range(winning.shape[0]):
    count_matched_numbers = count_matched_numbers_1d(scratched[i], winning[i])
    count_matched_numbers_per_card.append(count_matched_numbers)

def calculate_scores(count_matched_numbers_per_card):
    scores_per_line = []
    for count_matched_numbers in count_matched_numbers_per_card:
        score = 2**(count_matched_numbers - 1) if count_matched_numbers else 0
        scores_per_line.append(score)
    return scores_per_line

print(sum(calculate_scores(count_matched_numbers_per_card)))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2

copies_per_card = np.ones(len(count_matched_numbers_per_card), dtype=int)
n_cards = len(copies_per_card)
for i_card, matched_numbers in enumerate(count_matched_numbers_per_card):
    copies_per_card[i_card+1:min(i_card+1+matched_numbers, n_cards)] += copies_per_card[i_card]

print(sum(copies_per_card))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
