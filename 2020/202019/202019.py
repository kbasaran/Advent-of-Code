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

rule_dict = {}
for line in RULEBOOK.splitlines():
    no, rest = line.split(": ")
    no = int(no)
    rest = rest.replace("\"a\"", "201").replace("\"b\"", "202").split(" ")
    if (len(rest) == 2) & ("|" not in rest):
        rule_dict[no] = [[int(rest[0]), int(rest[1])]]

    elif (len(rest) == 3) & ("|" in rest):
        rule_dict[no] = [[int(rest[0])], [int(rest[2])]]

    elif (len(rest) == 5) & ("|" in rest):
        rule_dict[no] = [[int(rest[0]), int(rest[1])], [int(rest[3]), int(rest[4])]]

    elif (len(rest) == 1):
        rule_dict[no] = [[int(rest[0])]]

    else:
        raise ValueError(f"What is this line: {line}")


def apply_rule_to_position_in_list(comb, pos):
    global rule_dict
    new_liob = []
    if comb[pos] in rule_dict.keys():
        for rule_val in rule_dict[comb[pos]]:
            new_liob.append(comb[:pos] + rule_val + comb[pos+1:])
        return new_liob
    else:
        return []


def check_if_message_matches(message):
    possibles = [[8, 11]]
    pos = 0
    while 1:
        comb = possibles.pop()  # take the latest combination out of the possibilities stack
        if comb[pos] != message[pos]:  # if the value at position does not match the message we are checking against
            # Check for a new combination by replacing the latest value we checked from the dictionary
            new_combs = apply_rule_to_position_in_list(comb, pos)
            if len(new_combs) == 0:  # if not found in the dictionary
                pos = 0
            else:
                for new_comb in new_combs:
                    possibles.append(new_comb)  # add the new combinations to our possibilities list
        else:  # position for this combination was correct
            pos += 1  # move to the next position (for the same combination, that will be)
            if pos == len(message):  # if reached the end of the message, message is valid
                return True
            elif pos < len(comb):  # if we are not at the end of this combination
                possibles.append(comb)  # put the combination back in the stack. we'll continue checking it and creating variables of it
            else:  # exhausted this combination. don't put it back in the list.
                pos = 0
        if len(possibles) == 0:
            return False


counter = 0
for message_enc in MESSAGES_ENC:
    counter += check_if_message_matches(message_enc)

print(counter)
print(f"Elapsed time: {time.time() - start:.4g}s")

# %% Part 2
