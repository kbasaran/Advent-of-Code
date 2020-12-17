# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:05:01 2020

@author: kbasa
"""

with open("input.txt") as f:
    p_in = f.read()


leftover, nearby_ts = p_in.split("\nnearby tickets:\n")
classes, my_t = leftover.split("\nyour ticket:\n")

classes = classes.splitlines()
my_t = my_t.split(",")
nearby_ts = [line.split(",") for line in nearby_ts.splitlines()]

accepted_vals = set()
for line in classes:
    leftover, p2 = line.split(" or ")
    p1 = leftover.split(": ")[1]
    p1 = [int(i) for i in p1.split("-")]
    p2 = [int(i) for i in p2.split("-")]
    accepted_vals.update(list(range(p1[0], p1[1]+1)))
    accepted_vals.update(list(range(p2[0], p2[1]+1)))

# %% Part 1
invalid_sum = 0
invalid_tickets = set()
for i, ticket in enumerate(nearby_ts):
    invalid_ticket = False
    for val in ticket:
        if not int(val) in accepted_vals:
            invalid_sum += int(val)
            invalid_tickets.add(i)

print(invalid_sum)

# %% Part 2

# Remove the invalid tickets
for i in sorted(list(invalid_tickets), reverse=True):
    nearby_ts.pop(i)

# Make a dictionary to store information on what values are possible for each class
accepted_vals_dict = dict()
for line in classes:
    field_name, leftover = line.split(": ")
    p1, p2 = leftover.split(" or ")
    p1 = [int(i) for i in p1.split("-")]
    p2 = [int(i) for i in p2.split("-")]

    accepted_vals = set()
    accepted_vals.update(list(range(p1[0], p1[1]+1)))
    accepted_vals.update(list(range(p2[0], p2[1]+1)))

    accepted_vals_dict[field_name] = accepted_vals

# Find which classes are possible for a position in your ticket
possible_classes_for_a_position = {}
class_names = accepted_vals_dict.keys()
for i in range(len(my_t)):
    values_seen_at_this_position =\
        [int(ticket[i]) for ticket in (nearby_ts + [my_t])]
    valid_classes = []
    for clas in class_names:
        if all([(val in accepted_vals_dict[clas]) for val in values_seen_at_this_position]):
            valid_classes.append(clas)
    possible_classes_for_a_position[i] = valid_classes

# Find the classes that are possible only for one position and remove them from being possibility for the others
for _ in range(len(my_t)):
    for pos, clas_list in possible_classes_for_a_position.items():
        if len(clas_list) == 1:
            found = clas_list[0]
            for posis in range(len(my_t)):
                if (posis != pos) & (found in possible_classes_for_a_position[posis]):
                    possible_classes_for_a_position[posis].remove(found)

# Multiply the numbers on my ticket that start with "departure"
departures_product = 1
for i, val in enumerate(my_t):
    if possible_classes_for_a_position[i][0][:9] == "departure":
        departures_product *= int(val)

print(departures_product)
