# since the blocking VLs are listed in the file for each case
# (1) for each target virtual link, iterate through every link and determine the blocking status (and add to set) 
# (2) for each blocking stage, we compute the blocking based on the accumulation and RTA equation 
# (3) repeat (2) until all stages complete 
# create all configurations and for each configuration, we calculate a wcd for each virtual link 
'''
Assume the input file has the form already ordered by priority:
index, execution time(C), Period(T)
We will output the worst case delay value for each stream
'''
import argparse
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

SWITCH_A = 100
SWITCH_B = 200
ES1 = 1
ES2 = 2
ES3 = 3
ES4 = 4

class Virtual_link():

    def __init__(self, index, exec_time, period, source, destinations, priority):
        self.index = index
        self.exec_time = exec_time
        self.period = period
        self.source = source
        self.destinations = destinations
        self.destination = self.destinations[0] if len(self.destinations) == 1 else None
        self.priority = priority
        self.WCDs = {} # each destination maps to a wcd value

class Architecture():

    def __init__(self, architecture_path):
        # csv has "VL,Source,Destination,Period,ET,Priority" format, and Destination can be multiple
        self.arch_dict = {}
        with open(architecture_path, 'r') as arch: 
            arch_info =  csv.reader(arch, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            tmp = []
            for row in arch_info:
                tmp.append(row)
            for virtual_link in tmp[1:]: #Bug?? Skip the first line?
                index = int(virtual_link[0])
                source = int(virtual_link[1])
                destinations = virtual_link[2].split("#") #Bug?? Split works?
                destinations = [int(i) for i in destinations]
                period = float(virtual_link[3])
                exec_time = float(virtual_link[4])
                priority = int(virtual_link[5]) # 1 => high priority; 0 => low priority
                self.arch_dict[index] = Virtual_link(index, exec_time, period, source, destinations, priority)
        self.wcd_all = {}

    def find_next_pos(self, curr_pos, destination):
        if curr_pos == ES1 or curr_pos == ES3:
            return SWITCH_A
        elif curr_pos == ES2 or curr_pos == ES4:
            return SWITCH_B
        elif curr_pos == SWITCH_A:
            if destination == ES1 or destination == ES3:
                return destination
            else:
                return SWITCH_B
        else:
            if destination == ES2 or destination == ES4:
                return destination
            else:
                return SWITCH_A
    
    def check_block(self, target_link, block_link, curr_pos):
        destination = target_link.destination 
        next_pos = self.find_next_pos(curr_pos, destination)
        # if target_link.index == 9:
        #     print(f"{curr_pos}, {next_pos}, {target_link.destination}")
        block_curr = block_link.source
        block_destination = block_link.destination
        while block_curr != block_destination:
            if block_curr == curr_pos and next_pos == self.find_next_pos(block_curr, block_destination):
                return True
            block_curr = self.find_next_pos(block_curr, block_destination)                
        return False
    
    def compute_recurrent(self, maxC, I_curr, I_prev, execution_list, period_list, count):
        if I_curr == I_prev and (count != 0):
            return I_curr
        else:
            summation =  np.sum(np.dot(np.int_(I_curr/period_list)+1,execution_list))
            I_prev = I_curr
            I_curr = maxC+summation
            return self.compute_recurrent(maxC, I_curr, I_prev, execution_list, period_list, count+1)
    
    def rta_computation(self, target_link, curr_pos, arch_config):
        # arch_config format: VL index |-> Virtual Link Object
        blocking_set_heq = set() # multiple links are possible and form a set
        blocking_set_lower = None
        source = target_link.source
        for key in arch_config.arch_dict.keys(): 
            if key != target_link.index:
                # decide if it will block the target link 
                block_link = arch_config.arch_dict[key]
                if self.check_block(target_link, block_link, curr_pos):
                    # if target_link.index == 9:
                    #     print(f"{block_link.index}, {curr_pos}")
                    if block_link.priority < target_link.priority:
                        blocking_set_lower = block_link if blocking_set_lower == None or block_link.exec_time > blocking_set_lower.exec_time else blocking_set_lower                        
                    if block_link.priority >= target_link.priority:
                        blocking_set_heq.add(block_link)
        # for key in arch_config.arch_dict.keys(): 
        #     if key != target_link.index:
        #         if block_link.priority >= target_link.priority:
        #             blocking_set_heq.add(block_link)
        # already have high/equal priority links + maximum low link
        # compute recurrent for this level
        input_executaion_list = [link.exec_time for link in blocking_set_heq]
        maxC = blocking_set_lower.exec_time if blocking_set_lower != None  else 0.0
        input_period_list = [link.period for link in blocking_set_heq]
        return self.compute_recurrent(maxC, 0, 0, np.array(input_executaion_list), np.array(input_period_list), 0)

    def shrink_wcd_new(self, blockings, target_link): # for brutal force algorithm
        if len(blockings) == 3:
        # use new inequalities to further shrink the wcd, for 3-hop case
            B1 = blockings[0]
            B2 = blockings[1]
            B3 = blockings[2]
            if target_link.exec_time >= max(blockings[1:]):
                return B1+3*target_link.exec_time
            elif target_link.exec_time <= min(blockings[1:]):
                return sum(blockings)+target_link.exec_time
            elif target_link.exec_time >= B2 and target_link.exec_time <= B3:
                return B1+3*target_link.exec_time if B2+B3 <= 2*target_link.exec_time else sum(blockings)+target_link.exec_time
            else:
                return B1+B2+2*target_link.exec_time
        else:
            B1 = blockings[0]
            B2 = blockings[1]
            if target_link.exec_time >= B2:
                return B1+2*target_link.exec_time
            else:
                return B1+B2+target_link.exec_time
    
    def blocking_analysis_general(self, block_list, C): # for general computation 
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

    def worst_delay_helper(self, target_link, destination, arch_config):
        # compute wcd for a specific config with a specified destination
        source = target_link.source
        curr_pos = source
        rta_res = []
        while curr_pos != destination:
            rta_res.append(self.rta_computation(target_link, curr_pos, arch_config))
            # Move current position to next level
            curr_pos = self.find_next_pos(curr_pos, destination)
        if target_link.index == 9:
            print(rta_res)
        final_wcd = self.blocking_analysis_general(rta_res, target_link.exec_time)
        # map this wcd to the corresponding result destination 
        return final_wcd
        
    def compute_target_link(self, index, arch_config):
        target_link = self.arch_dict[index]
        destinations = target_link.destinations
        for destination in destinations:
            # compute the wcd for this specific case 
            target_link.destination = destination
            wcd = self.worst_delay_helper(target_link, destination, arch_config)
            # update wcd in this virtual link with such destination
            self.arch_dict[target_link.index].WCDs[destination] = wcd if destination not in self.arch_dict[target_link.index].WCDs else max(wcd, self.arch_dict[target_link.index].WCDs[destination])

    def worst_case_delay_all(self, arch_config):
        for index in self.arch_dict.keys():
            # update the target link with every destination in this config 
            self.compute_target_link(index, arch_config)


if __name__ == "__main__":
    architecture_name = "architecture.csv"
    architecture_path = os.path.join("", architecture_name)
    # initialize the archtecture
    arch = Architecture(architecture_path)
    # construct configurations 
    multiple_dest_dict = {}

    for index in arch.arch_dict.keys(): #bug?? how to obtain all keys
        # collect all virtual links with destinations more than 1 and form all configs based on that
        if len(arch.arch_dict[index].destinations) > 1: 
            multiple_dest_dict[index] = arch.arch_dict[index].destinations
    # each unique key should have a value matched to it in every config
    # traverse each config and compute each worst case delay
    # {1: E1, E2; 2: E2, E3} => 
            # (1) {1: E1; 2: E2} 
            # (2) {1: E2; 2: E2} 
            # (3) {1: E1; 2: E3} 
            # (4) {1: E2; 2: E3} 
    arch_configs = [dict(zip(multiple_dest_dict.keys(), p)) for p in product(*multiple_dest_dict.values())]
    for idx, perm in enumerate(arch_configs, start=1):
        print(f'({idx}) {perm}')
        arch_config = Architecture(architecture_path)
        # iterate each config and assign the destination to each possible result
        for index in perm.keys():
            arch_config.arch_dict[index].destination = perm[index]
        arch.worst_case_delay_all(arch_config)
    
    # Print out each result with corresponding destination 
    wcd_all = [(index, arch.arch_dict[index].WCDs) for index in arch.arch_dict.keys()]
    max_wcd_all = [(index, max(arch.arch_dict[index].WCDs.values())) for index in arch.arch_dict.keys()]

    print("All possible destinations considered", sorted(wcd_all))
    print("The maximum of all destinations considered", [ v for (k, v) in sorted(max_wcd_all)])
            