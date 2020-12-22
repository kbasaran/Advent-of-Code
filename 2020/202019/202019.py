import time

start = time.time()

with open("input.txt") as f:
    P_IN = f.read()

RULEBOOK, MESSAGES = P_IN.strip().split("\n\n")

MESSAGES = MESSAGES.splitlines()
MESSAGES_ENC = [list(line) for line in MESSAGES]
for line in MESSAGES_ENC:
    for pos in range(len(line)):
        if line[pos] == "b":
            line[pos] = 202
        else:
            line[pos] = 201

RULE_DICT = {}
for line in RULEBOOK.splitlines():
    no, rest = line.split(": ")
    no = int(no)
    rest = rest.replace("\"a\"", "201").replace("\"b\"", "202").split(" ")
    if (len(rest) == 2) & ("|" not in rest):
        RULE_DICT[no] = [[int(rest[0]), int(rest[1])]]

    elif (len(rest) == 3) & ("|" in rest):
        RULE_DICT[no] = [[int(rest[0])], [int(rest[2])]]

    elif (len(rest) == 5) & ("|" in rest):
        RULE_DICT[no] = [[int(rest[0]), int(rest[1])], [int(rest[3]), int(rest[4])]]

    elif (len(rest) == 1):
        RULE_DICT[no] = [[int(rest[0])]]

    else:
        raise ValueError(f"What is this line: {line}")


def apply_rule_to_position_in_list(comb, pos):
    global RULE_DICT
    new_combs = []
    if comb[pos] in RULE_DICT.keys():
        for rule_val in RULE_DICT[comb[pos]]:
            new_combs.append(comb[:pos] + rule_val + comb[pos+1:])
        return new_combs
    else:
        return []


def check_if_message_matches(message, to_match):
    possibles = list(to_match)
    pos = 0
    while 1:

        comb = possibles[-1]  # use the list as a stack

        if comb[pos] == message[pos]:  # for this combination in our stack, value at position 'pos' is matching the message

            if (pos == len(message) - 1) & (pos == len(comb) - 1):  # we reached the end of the message. message is valid.
                return True

            elif (pos < len(comb) - 1) & (pos < len(message) - 1):  # valid until now but still and need to check further positions of the message.
                pos += 1  # move to the next position (still checking the same combination, only moving to next letter)

            else:  # exhausted this combination. discard it.
                possibles.pop()
                pos = 0

        else:  # value at position 'pos' does not match the message we are checking against

            possibles.pop()  # remove this combination from the stack

            if new_combs := apply_rule_to_position_in_list(comb, pos):  # and try to replace
                for new_comb in new_combs:
                    possibles.append(new_comb)  # add the new combinations to our possibilities list

            else:
                pos = 0

        if len(possibles) == 0:
            return False


# %% Part 1
counter = 0
to_match = [[8, 11]]
for message_enc in MESSAGES_ENC:
    counter += check_if_message_matches(message_enc, to_match)

print(f"Answer: {counter}")
print(f"Elapsed time: {time.time() - start:.4g}s")


# %% Part 2
start2 = time.time()

# Possible combinations are a list of [n*42, m*42, m*31]
# Add combinations based on this to the list the function will check against
to_match = []
for n in range(1, 9):
    for m in range(1, 9):
        comb = [42] * (n+m) + [31] * m
        to_match.append(comb)

counter = 0
for message_enc in MESSAGES_ENC:
    counter += check_if_message_matches(message_enc, to_match)

print(f"Answer: {counter}")
print(f"Elapsed time: {time.time() - start2:.4g}s")
