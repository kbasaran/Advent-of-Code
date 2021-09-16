input = "L5, R1, R3, L4, R3, R1, L3, L2, R3, L5, L1, L2, R5, L1, R5, R1, L4, R1, R3, L4, L1, R2, R5, R3, R1, R1, L1, R1, L1, L2, L1, R2, L5, L188, L4, R1, R4, L3, R47, R1, L1, R77, R5, L2, R1, L2, R4, L5, L1, R3, R187, L4, L3, L3, R2, L3, L5, L4, L4, R1, R5, L4, L3, L3, L3, L2, L5, R1, L2, R5, L3, L4, R4, L5, R3, R4, L2, L1, L4, R1, L3, R1, R3, L2, R1, R4, R5, L3, R5, R3, L3, R4, L2, L5, L1, L1, R3, R1, L4, R3, R3, L2, R5, R4, R1, R3, L4, R3, R3, L2, L4, L5, R1, L4, L5, R4, L2, L1, L3, L3, L5, R3, L4, L3, R5, R4, R2, L4, R2, R3, L3, R4, L1, L3, R2, R1, R5, L4, L5, L5, R4, L5, L2, L4, R4, R4, R1, L3, L2, L4, R3"
# input = "R8, R4, R4, R8"

from collections import namedtuple
import sys

Position = namedtuple("position", ["x", "y", "dir"])


def move(position, instruction):
    dir_new = position.dir * {"L": 1j, "R": -1j, "S": 1, "B": -1}.get(instruction[0])

    distance = int(instruction[1:])
    x_new = position.x + distance * dir_new.real
    y_new = position.y + distance * dir_new.imag

    print(f"New pos: ({x_new}, {y_new}), Dir: {dir_new}")
    return Position(x_new, y_new, dir_new)


# %% Part 1
pos = Position(0, 0, 1j)
for instruction in input.split(", "):
    pos = move(pos, instruction)
print(f"Street distance is {int(abs(pos.x) + abs(pos.y))} blocks.")

# %% Part 2
pos = Position(0, 0, 1j)
visited_locations = {(0, 0)}
for instruction in input.split(", "):
    for step_no in range(int(instruction[1:])):
        if step_no == 0:
            pos = move(pos, instruction[0] + "1")
        else:
            pos = move(pos, "S" + "1")

        new_loc_tuple = (pos.x, pos.y)
        if new_loc_tuple in visited_locations:
            print(f"You had been to {pos.x}, {pos.y} before!!")
            print(f"Street distance is {int(abs(pos.x) + abs(pos.y))} blocks.")
            sys.exit()
        else:
            visited_locations.add(new_loc_tuple)
