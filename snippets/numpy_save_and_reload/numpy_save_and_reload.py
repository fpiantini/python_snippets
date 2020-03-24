#!/usr/bin/env python3

import sys
import random
import numpy as np

ztable= np.empty([3, 3, 2], dtype=int)
random.seed()

print("*************** GENERATED RANDOM ZOBRIST HASH TABLE ***************")
for _x in range(0, 3):
    for _y in range(0, 3):
        for _e in range(0, 2):
            ztable[_x][_y][_e] = random.randint(0, sys.maxsize)
print(ztable)

print("")
print("******************** GENERATED RANDOM VECTOR **********************")
vec = np.random.rand(100)
print(vec)

# *****************************************************************
# saves everything
np.savez('numpydata', zobrist_hash = ztable, random_vector = vec)
# *****************************************************************

print("")
print("")

try:
    # *************************************************************
    # reloads everything
    saved_data = np.load('numpydata.npz')
    # *************************************************************
except:
    print("error reading data from numpydata file")
    quit()

print("************************* RELOADED  TABLE *************************")
print(saved_data['zobrist_hash'])
print("")
print("************************* RELOADED VECTOR *************************")
print(saved_data['random_vector'])

