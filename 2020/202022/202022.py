import queue
from pathlib import Path
import time
from dataclasses import dataclass
import copy
import functools

start1 = time.time()

def read_input(file_name):
    P_IN = Path.cwd().joinpath(file_name).read_text()
    p1 = P_IN.split("\n\nPlayer")[0].replace("Player 1:\n", "").splitlines()
    p1 = tuple([int(val) for val in p1])
    p2 = P_IN.split("\n\nPlayer 2:\n")[1].splitlines()
    p2 = tuple([int(val) for val in p2])
    return p1, p2


def make_hand(card_list):
    hand = queue.SimpleQueue()
    for card in card_list:
        hand.put(card)
    return hand

# Main
p1_cards, p2_cards = read_input("input_test.txt")
p1_hand = make_hand(p1_cards)
p2_hand = make_hand(p2_cards)

# Start game

turn = 0
while (p1_hand.qsize() * p2_hand.qsize()) > 0:
    turn += 1
    p1_card = p1_hand.get()
    p2_card = p2_hand.get()

    if p1_card > p2_card:
        winner_cards = p1_hand
        winner_card = p1_card
        loser_card = p2_card
    elif p2_card > p1_card:
        winner_cards = p2_hand
        winner_card = p2_card
        loser_card = p1_card
    else:
        print(f"Error. p1: {p1_card}, p2: {p2_card}")
    winner_cards.put(winner_card)
    winner_cards.put(loser_card)


scores = []
for hand in [p1_hand, p2_hand]:
    score = 0
    hand_size = hand.qsize()
    for i in range(hand_size):
        score += hand.get() * (hand_size - i)
    scores.append(score)


print("Part 1 scores:")
print(scores)
print(f"Elapsed time: {time.time() - start1:.4g}s")

# %% Part 2
start2 = time.time()

@dataclass
class Hand():
    cards: tuple

    def __post_init__(self):
        self.cards = list(self.cards)
        self.history = set()
        self.recurred = False
        self.update_props()

    def get(self):
        card = self.cards[0]
        self.cards = self.cards[1:]
        self.update_props()
        return card

    def add(self, new_card):
        self.cards = self.cards + [new_card]
        self.update_props()

    def update_props(self):
        self.len = len(self.cards)

    def give_card_list(self):
        return tuple(self.cards)

    def clone(self, n_cards):
        new_copy = copy.deepcopy(self)
        new_copy.history = set()
        new_copy.cards = new_copy.cards[:n_cards]
        return new_copy


def calc_score(cards):
    score = 0
    for i in range(len(cards)):
        score += cards[i] * (len(cards) - i)
    return score


# Main, part 2

p1_cards, p2_cards = read_input("input.txt")
p1_hand = Hand(p1_cards)
p2_hand = Hand(p2_cards)

game = 0


def play(p1_hand, p2_hand):
    global game
    game += 1
    played_games = set()

    turn = 0
    while ((p1_hand.len * p2_hand.len) > 0):
        turn += 1

        hands_state = p1_hand.give_card_list() + (0, 0) + p2_hand.give_card_list()
        curr_hash = hash(hands_state)

        if curr_hash in played_games:
            winner = 1
            winner_cards = p1_hand.give_card_list()
            break

        else:
            played_games.add(curr_hash)

            p1_card = p1_hand.get()
            p2_card = p2_hand.get()

            if (p1_hand.len >= p1_card) and (p2_hand.len >= p2_card):
                winner, _ = play(p1_hand.clone(p1_card), p2_hand.clone(p2_card))
            elif p1_card > p2_card:
                winner = 1
            elif p2_card > p1_card:
                winner = 2
            else:
                print(f"Error1. p1: {p1_card}, p2: {p2_card}")

        if winner == 1:
            p1_hand.add(p1_card)
            p1_hand.add(p2_card)
            winner_cards = p1_hand.give_card_list()
        elif winner == 2:
            p2_hand.add(p2_card)
            p2_hand.add(p1_card)
            winner_cards = p2_hand.give_card_list()
        else:
            print(f"Error2. p1: {p1_card}, p2: {p2_card}")

    return(winner, winner_cards)


winner, winner_cards = play(p1_hand, p2_hand)

print()
print(f"Part 2 winner: {winner}\nScore: {calc_score(winner_cards)}")
print(f"Elapsed time: {time.time() - start2:.4g}s")
