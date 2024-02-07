# the input type is: 
# (1) a list of blocking time for each hop; 
# (2) C for the frame from target VL;

import argparse
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

def blocking_analysis(block_list, C):
    Block = []
    curr_wcd = 0
    current_sum = 0
    for num in block_list:
        current_sum += num
        Block.append(current_sum)
    print(Block)
    for k in range(len(block_list)):
        print(curr_wcd)
        if k == 0: 
            curr_wcd += C+block_list[k]
        else:
            curr_wcd = C + max(curr_wcd, Block[k])
    return curr_wcd

A = [10, 10, 10]
C = 5
print(blocking_analysis(A, C))