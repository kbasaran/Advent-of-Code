# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()


# %% Part 1
pos = {'hor_pos': 0, 'depth': 0}
commands = [command_line.split() for command_line in p_in.splitlines()]

for direction, amount in commands:
    pos['hor_pos'] += (direction == 'forward') * int(amount)
    pos['depth'] += ((direction == 'down') - (direction == 'up')) * int(amount)

print("Part 1: " + str(pos['depth'] * pos['hor_pos']))

# %% Part 2
pos = {'hor_pos': 0, 'depth': 0}
aim = 0

for direction, amount in commands:
    pos['hor_pos'] += (direction == 'forward') * int(amount)
    pos['depth'] += aim * (direction == 'forward') * int(amount)
    aim += ((direction == 'down') - (direction == 'up')) * int(amount)

print("Part 2: " + str(pos['depth'] * pos['hor_pos']))
