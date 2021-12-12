# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

# global
lines = {}


def analyze_new_char(line_no, new_char):
    global lines
    open_chars = "[{<("
    close_chars = "]}>)"
    current_list = lines[line_no]
    if new_char in open_chars:
        current_list.append(new_char)
    if new_char in close_chars:
        open_version = open_chars[close_chars.find(new_char)]
        if open_version == current_list[-1]:
            current_list.pop()
        else:
            return new_char


def parse_input(p_in):
    return p_in.splitlines()


def part_1(p_in):
    global corrupt_row_nos, lines
    points_dict = {"]": 57,
                   ")": 3,
                   "}": 1197,
                   ">": 25137,
                   }
    points = 0
    corrupt_row_nos = []
    for i, row in enumerate(parse_input(p_in)):
        lines[i] = []
        for new_char in row:
            error = analyze_new_char(i, new_char)
            if error:
                points += points_dict[error]
                corrupt_row_nos.append(i)
                break

    print(f"\n--Part 1--\nAnswer: {points}")


def part_2():
    global corrupt_row_nos, lines

    points_dict = {"[": 2,
                   "(": 1,
                   "{": 3,
                   "<": 4,
                   }

    all_points = []
    for i, row in enumerate(parse_input(p_in)):
        if i not in corrupt_row_nos:
            points = 0
            vals = reversed(lines[i])
            for val in vals:
                points *= 5
                points += points_dict[val]
            all_points.append(points)

    mid_value = sorted(all_points)[len(all_points) // 2]

    print(f"\n--Part 2--\nAnswer: {mid_value}")


part_1(p_in)
part_2()

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
