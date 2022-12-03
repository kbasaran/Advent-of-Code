# 2022 Day 03

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()

def priority(letter):
    if letter.islower():
        return ord(letter) - 96
    elif letter.isupper():
        return ord(letter) - 38
    else:
        raise ValueError

def find_repeated_item(r1, r2):
    if repeated_item := r1.intersection(r2):
        assert len(repeated_item) == 1
        return priority(repeated_item.pop())
    else:
        raise ValueError

elves = []
priorities_sum = 0
for rucksack_text in p_in.splitlines():
    len_each = len(rucksack_text) // 2
    r1 = set(rucksack_text[:len_each])
    r2 = set(rucksack_text[-len_each:])
    elves.append((r1, r2))
    priorities_sum += find_repeated_item(r1, r2)

print(priorities_sum)  # Answer part 1

priorities_sum = 0
for elf_group in [elves[i*3:i*3+3] for i in range(len(elves)//3)]:
    whole_sacks = [r1.union(r2) for r1, r2 in elf_group]
    badge = whole_sacks[0].intersection(whole_sacks[1], whole_sacks[2])
    assert len(badge) == 1
    priorities_sum += priority(badge.pop())

print(priorities_sum)  # Answer part 2

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
