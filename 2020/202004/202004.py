# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 11:03:39 2020

@author: kerem.basaran
"""

with open("input.txt") as f:
    pds = []

    for string in f.read().split("\n\n"):
        ps = string.strip().replace("\n", " ").split(" ")
        ps_dict = {}

        for key, val in [i.split(":") for i in ps]:
            ps_dict[key] = val
        pds.append(ps_dict)

# %% Part 1
valid = 0
required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

for psport in pds:
    if all([field in psport.keys() for field in required_fields]):
        valid += 1

print(valid)

# %% Part 2
valid_pps = []
for psport in pds:
    policy = 0

    if not all([field in psport.keys() for field in required_fields]):
        continue
    policy += 1

    if "".join([psport[i] for i in ["byr", "iyr", "eyr"]]).isdigit() and \
        all([
            1920 <= int(psport["byr"]) <= 2002,
            2010 <= int(psport["iyr"]) <= 2020,
            2020 <= int(psport["eyr"]) <= 2030
            ]):
        policy += 2

    if (val_hgt := psport["hgt"][:-2]).isdigit():
        unit_hgt = psport["hgt"][-2:]
        if ((unit_hgt == "cm") & (150 <= int(val_hgt) <= 193)) or \
                ((unit_hgt == "in") & (59 <= int(val_hgt) <= 76)):
            policy += 4

    hair = psport["hcl"][0], psport["hcl"][1:]
    valid_chars = "abcdef0123456789"
    if all([(char in valid_chars) for char in hair[1]]) and (hair[0] == "#"):
        policy += 8

    pid = psport["pid"]
    if (pid.isdigit() & (len(pid) == 9)):
        policy += 16

    valid_ecls = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    if any([psport["ecl"] == ecl for ecl in valid_ecls]):
        policy += 32

    if policy == 64 - 1:
        valid_pps.append(psport)

print(len(valid_pps))
