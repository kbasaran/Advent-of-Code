# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 19:25:51 2020

@author: kerem.basaran
"""

with open("input.txt") as f:
    p_in = f.read().splitlines()


def apply_bitmask(data, mask):
    out = 0
    for pos, val in enumerate(mask):
        if val in "01":  # change the bit in data to the value in mask
            bit = int(val)
        elif val == "X":  # keep the bit in data the same as it was
            bit = 1 & (data >> (len(mask) - pos - 1))
        out = (out << 1) + bit
    return out


memory = {}
for line in p_in:
    if line[:4] == "mask":  # new mask seen in list, make it the active one
        cur_mask = line[-36:]
    else:
        address = int(line.split("] ")[0].replace("mem[", ""))
        val = int(line.split(" = ")[1])
        memory[address] = apply_bitmask(val, cur_mask)
print(sum(memory.values()))


# %% Part 2
def possible_mem_addresses(address, mask_raw):
    # Adress combinations due to "0" and "1"s in the bitmask
    address_modified = ""
    mask = mask_raw.zfill(36)
    for i, val in enumerate(mask):
        if val in "1X":  # if 1 or X just make it 1. X values will be handled later.
            address_modified += "1"
        elif val == "0":
            address_modified += format(address, "36b")[i]
    address_modified = int(address_modified.replace(" ", "0"), 2)

    # Create masks that have combination of "0"s and "1"s where the "X" values are.
    # These masks are only for internal use. They will be applied to "address_modified".
    # This will generate the final masks that get applied to the memory address.
    mem_addr_masks = []  # these are masks to modify the "X" values in the address and create combinations
    count_x = mask.count("X")  # how many combinations there will be
    floating_positions = [i for i, val in enumerate(mask) if val == "X"]
    for i in range(2**len(floating_positions)):  # for each combination
        new_vals = format(i, "36b")[-count_x:].replace(" ", "0")
        new_mask = "X" * len(mask)
        for j, new_val in enumerate(new_vals):  # write the 0's and 1's to location of each "X"
            new_mask = new_mask[:floating_positions[j]] + new_vals[j] + new_mask[floating_positions[j]+1:]
        mem_addr_masks.append(new_mask)

    # For each address, generate the combinations due to the floating "X"'s
    out = []
    for mem_addr_mask in mem_addr_masks:
        out.append(apply_bitmask(address_modified, mem_addr_mask))
    return out


memory = {}
for line in p_in:
    if line[:4] == "mask":  # new mask seen in list, make it the active one
        cur_mask = line[-36:]
    else:  # read the address and value defined in the line
        address = int(line.split("] ")[0].replace("mem[", ""))
        val = int(line.split(" = ")[1])
        for addr in possible_mem_addresses(address, cur_mask):
            # write this value to all possible memory locations
            memory[addr] = val
print(sum(memory.values()))
