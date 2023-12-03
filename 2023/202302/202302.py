# 2023 Day 02

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

# ---- Part 1

def max_revealed_per_color(line: str) -> (int, dict):
    # line represents input for one game
    game_id, box_text = line.removeprefix("Game ").split(":")
    game_id = int(game_id)
    boxes_revealed = {"red": 0, "green": 0, "blue": 0}
    for text_per_turn in box_text.split(";"):
        reveals = text_per_turn.split(",")
        for reveal in reveals:
            amount, color = reveal.split()
            boxes_revealed[color] = max(int(amount), boxes_revealed[color])

    return game_id, boxes_revealed


def is_it_possible(boxes_revealed: dict, n_red: int, n_green: int, n_blue: int) -> bool:
    if boxes_revealed["red"] > n_red:
        return False
    elif boxes_revealed["green"] > n_green:
        return False
    elif boxes_revealed["blue"] > n_blue:
        return False
    else:
        return True

possible_games = set()
boxes_revealed_per_game = {}

for line in p_in.splitlines():
    game_id, boxes_revealed = max_revealed_per_color(line)
    if is_it_possible(boxes_revealed, 12, 13, 14):
        possible_games.add(game_id)
    boxes_revealed_per_game[game_id] = boxes_revealed  # store for part 2

print(sum(possible_games))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.\n")


# ---- Part 2

powers = []
for boxes_revealed in boxes_revealed_per_game.values():
    power = boxes_revealed["red"] * boxes_revealed["green"] * boxes_revealed["blue"]
    powers.append(power)

print(sum(powers))
print(f"Solved in {(perf_counter() - start_time) * 1000:.3g} ms.")
