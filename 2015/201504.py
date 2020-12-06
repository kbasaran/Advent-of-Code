# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:03:12 2020

@author: kbasa
"""

import hashlib


def check_hash(seed):
    hash = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return (hash[:6] == "000000", hash)

p_in = "ckczppom"
num = 0
while 1:
    num += 1
    seed = p_in + str(num)
    if check_hash(seed)[0]:
        print(num, check_hash(seed)[1])
        break
