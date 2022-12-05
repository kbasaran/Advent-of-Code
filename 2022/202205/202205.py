# 2022 Day 05

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

def parse_start_stacks(stacks_text: str):
    lines = stacks_text.splitlines()[::-1]
    n_stacks = max([int(val) for val in lines[0].replace(" ", "")])
    stacks = {i: [] for i in range(1, n_stacks + 1)}
    for line in lines[1:]:
        for i_stack, stack in stacks.items():
            line_pos = 4 * i_stack - 3
            if (letter := line[line_pos]) != " ":
                stack.append(letter)
    return stacks

def parse_movement_commands(commands_text: str):
    commands = []
    for line in commands_text.splitlines():
        n_crate = int(line.split()[1])
        fro_stack = int(line.split()[-3])
        to_stack = int(line.split()[-1])
        commands.append((n_crate, fro_stack, to_stack))
    return commands

def crane_operation(stacks, n_crate, from_stack, to_stack, crane_version=9000):
    moving = stacks[from_stack][-n_crate:]
    del stacks[from_stack][-n_crate:]
    if crane_version == 9000:
        stacks[to_stack] += reversed(moving)
    elif crane_version == 9001:
        stacks[to_stack] += moving
    else:
        raise TypeError("Unrecognized crane version.")


if __name__ == "__main__":
    stack_text, comm_text = p_in.split("\n\n")    
    stacks = parse_start_stacks(stack_text)
    commands = parse_movement_commands(comm_text)
    
    for command in commands:
        crane_operation(stacks, *command)
    print("".join([stack[-1] for stack in stacks.values()]))  # Part 1

    stacks = parse_start_stacks(stack_text)
    for command in commands:
        crane_operation(stacks, *command, crane_version=9001)
    print("".join([stack[-1] for stack in stacks.values()]))  # Part 2


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
