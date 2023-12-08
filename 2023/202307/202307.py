# 2023 Day 07

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import polars as pl

start_time = perf_counter()

# ---- Part 1

class Hand:
    def __init__(self, cards: str, bid: int):
        assert len(cards) == 5
        self.cards = cards
        self.bid = int(bid)
        self.card_counts = self.count_cards(cards)
        self.raw_value = self.calc_raw_value(cards)
        self.score = self.calc_score(self.card_counts)

    def __repr__(self):
        return f"{self.cards}, score: {self.score}, bid: {self.bid}\n"

    def count_cards(self, cards):
        s = pl.Series("cards", cards)
        card_counts = s.value_counts()
        card_counts = dict(zip(card_counts.select(pl.col("cards")).to_series(),
                               card_counts.select(pl.col("counts")).to_series(),
                              )
                          )
        return card_counts

    def card_to_val(self, card):
        assert len(card) == 1
        vals = {"A": 14,
                "K": 13,
                "Q": 12,
                "J": 11,
                "T": 10,
                }
        if card in vals:
            return vals[card]
        else:
            return int(card)

    def calc_raw_value(self, cards):
        return sum([15**i * self.card_to_val(card) for i, card in enumerate(reversed(list(cards)))]) 

    def calc_score(self, card_counts):
        counts = card_counts.values()
        if 5 in counts:
            return 15**10 + self.raw_value
        elif 4 in counts:
            return 15**9 + self.raw_value
        elif 3 in counts and 2 in counts:  # full house
            return 15**8 + self.raw_value
        elif 3 in counts:
            return 15**7 + self.raw_value
        elif list(counts).count(2) == 2:
            return 15**6 + self.raw_value
        elif 2 in counts:
            return 15**5 + self.raw_value
        else:
            return self.raw_value

def parse_input(p_in, hand_class):
    hands = []
    for cards, bid in [line.split() for line in p_in.strip().splitlines()]:
    
        hand = hand_class(cards, bid)
        hands.append(hand)
    return hands

def winnings(hands):
    winnings = []
    for i, hand in enumerate(sorted(hands, key=lambda hand: hand.score)):
        winnings.append((i + 1) * hand.bid)
    return sum(winnings)

hands = parse_input(p_in, Hand)
print(winnings(hands))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")

# ---- Part 2

class Handj(Hand):
    
    def __init__(self, cards: str, bid: int):
        assert len(cards) == 5
        self.cards = cards
        self.bid = int(bid)
        self.card_counts = self.count_cards(cards)
        self.raw_value = self.calc_raw_value(cards)
        self.score = self.calc_score(self.hand_counts_after_applying_jokers_in_best_way_possible())

    def card_to_val(self, card):
        assert len(card) == 1
        vals = {"A": 14,
                "K": 13,
                "Q": 12,
                "J": 1,
                "T": 10,
                }
        if card in vals:
            return vals[card]
        else:
            return int(card)

    def hand_counts_after_applying_jokers_in_best_way_possible(self):
        if self.cards == "JJJJJ":
            return self.card_counts
        card_counts_no_joker = {key: val for key, val in self.card_counts.items() if key != "J"}
        most_occurring_card = max(card_counts_no_joker, key=card_counts_no_joker.get)
        occurrence_joker = self.cards.count("J")
        card_counts_no_joker[most_occurring_card] += occurrence_joker

        return card_counts_no_joker

hands = parse_input(p_in, Handj)
print(winnings(hands))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")
