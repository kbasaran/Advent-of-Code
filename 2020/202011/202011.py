import numpy as np

with open("input.txt") as f:
    p_in = f.read().replace(".", "0").replace("L", "1")\
           .replace("#", "2").splitlines()
    rows = [[int(i) for i in row] for row in p_in]


arr = np.array(rows)
x_max, y_max = [i-1 for i in arr.shape]

# x is row number, y is column number


def check_relatives(arr, pos, relative_pos_list):
    answers = []
    global x_max, y_max
    for rel_pos in relative_pos_list:
        pos_x, pos_y = pos[0] + rel_pos[0], pos[1] + rel_pos[1]
        if 0 <= pos_x <= x_max and 0 <= pos_y <= y_max:
            answers.append(arr[pos_x, pos_y])
        else:
            answers.append(None)
    return answers


def check_spacious(arr, pos):
    if arr[pos] == 0:
        return 0
    states = check_relatives(arr, pos, [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                        (0, 1), (1, -1), (1, 0), (1, 1)])
    if 2 in states:
        return arr[pos]
    else:
        return 2


def check_crowded(arr, pos):
    if arr[pos] == 0:
        return 0
    states = check_relatives(arr, pos, [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                        (0, 1), (1, -1), (1, 0), (1, 1)])
    if states.count(2) >= 4:
        return 1
    else:
        return arr[pos]


part1 = np.array(arr)
part1_n = np.zeros((x_max + 1, y_max + 1))
counter = 1
while 1:
    for x in range(x_max + 1):
        for y in range(y_max + 1):
            part1_n[x, y] = check_spacious(part1, (x, y))

    for x in range(x_max + 1):
        for y in range(y_max + 1):
            part1[x, y] = check_crowded(part1_n, (x, y))
    counter += 1
    if counter % 10 == 0:
        print()
        print(part1)
        print(f"Occupied seats: {np.count_nonzero(part1 == 2)}")
    if counter > 100:
        break


# %% Part 2
print("-------------Part 2---------------")
def check_visibles(arr, pos):
    states = [0] * 8
    dir_ref = ((0, 1), (-1, 1), (-1, 0), (-1, -1),
               (0, -1), (1, -1), (1, 0), (1, 1))
    dirs = list(dir_ref)
    while 0 in states:
        states = check_relatives(arr, pos, dirs)
        for i in range(len(dirs)):
            if states[i] == 0:
                dirs[i] = [dirs[i][j] + val for j, val in enumerate(dir_ref[i])]
    return states


def check_spacious_p2(arr, pos):
    if arr[pos] == 0:
        return 0
    states = check_visibles(arr, pos)
    if 2 in states:
        return arr[pos]
    else:
        return 2


def check_crowded_p2(arr, pos):
    if arr[pos] == 0:
        return 0
    states = check_visibles(arr, pos)
    if states.count(2) >= 5:
        return 1
    else:
        return arr[pos]


part2 = np.array(arr)
part2_n = np.zeros((x_max + 1, y_max + 1))
counter = 1
while 1:
    for x in range(x_max + 1):
        for y in range(y_max + 1):
            part2_n[x, y] = check_spacious_p2(part2, (x, y))

    for x in range(x_max + 1):
        for y in range(y_max + 1):
            part2[x, y] = check_crowded_p2(part2_n, (x, y))
    counter += 1
    if counter % 10 == 0:
        print()
        print(part2)
        print(f"Occupied seats: {np.count_nonzero(part2 == 2)}")
    if counter > 100:
        break
