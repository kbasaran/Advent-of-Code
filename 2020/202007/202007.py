# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 22:37:20 2020

@author: kerem.basaran
"""

from collections import namedtuple

with open("input.txt") as f:
    p_in = f.read().splitlines()

# %% Part 1
Bag = namedtuple("Bag", ["name", "parents", "contents"])
bags = {}


def add_new_bag(bag_name):
    bags[bag_name] = Bag(bag_name, [], [])


def add_parent(bag_name: str, parent_name: str):
    if bag_name not in bags:
        add_new_bag(bag_name)
    if parent_name not in bags:
        add_new_bag(parent_name)
    bags[bag_name].parents.append(bags[parent_name])


def add_content(bag_name: str, content_name: str):
    if bag_name not in bags:
        add_new_bag(bag_name)
    if content_name not in bags:
        add_new_bag(content_name)
    bags[bag_name].contents.append(bags[content_name])


def translate_line(line):
    start = 0
    section = "before_contain"
    words = line.split(" ")
    multiplier = 1
    for pos, word in enumerate(words):
        if word.isdigit():
            multiplier = int(word)
            start += 1
        elif "bag" in word:
            bag_name = " ".join(words[start:pos])
            start = pos + 1
            if bag_name != "no other":
                if section == "before_contain":
                    parent_name = bag_name
                if section == "after_contain":
                    add_parent(bag_name, parent_name)
                    for _ in range(multiplier):
                        add_content(parent_name, bag_name)
        elif "contain" in word:
            start += 1
            section = "after_contain"


for line in p_in:
    translate_line(line)

parents = set()


def find_parent(child):
    for bag in child.parents:
        parents.add(bag.name)
        find_parent(bag)


find_parent(bags["shiny gold"])
print(len(parents))

# %% Part 2
contents = []


def find_contents(parent):
    for bag in parent.contents:
        contents.append(bag.name)
        find_contents(bag)


find_contents(bags["shiny gold"])
print(len(contents))
