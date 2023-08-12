'''
Aiming to parse the input architecture into all possible cases and then compute
the worst case delay out of every possibility 
'''

import argparse
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from copy import *

# parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--architecture_input', type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    tmp=[]

    # read inputs 
    with open(args.architecture_input, 'r') as r: 
        architecture = csv.reader(r, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in architecture:
            tmp.append(row)

    # permute all cases
    architecture = tmp
    all_combo = {}
    for (VL, Source, Destination, Period, Exec_Time, Priority) in architecture:
        Destinations = Destination.split('#')
        if len(Destinations) > 1:
            all_combo[int(VL)] = Destinations
    permu = []
    for key in all_combo.keys():
        values = all_combo[key]
        if len(permu) == 0:
            for value in values:
                permu += [[(key,value)]]
        else:
            temp = []
            for i in range(len(permu)):
                e = permu[i]
                for j in range(len(values)):
                    tp = copy(e)
                    value = values[j]
                    tp += [(key,value)]
                    temp += [tp]
            permu = copy(temp)

    # construct different permutations
    permu = [{key:value for (key, value) in case} for case in permu]
    result = []

    # result = np.array(len())
    for case in permu:
        tmp = []
        for row in architecture[1:]:
            (VL, Source, Destination, Period, Exec_Time, Priority) = row
            if int(VL) in case:
                tmp.append((VL, Source, case[(int(VL))], Period, Exec_Time, Priority))
            else:
                tmp.append((VL, Source, Destination, Period, Exec_Time, Priority))
        result.append(tmp)
        print(tmp)
        print("------------------------line separate-------------------------")
    
    # separate all virtual links to different folders
    count = 0
    for scenario in result:
        folder_name = f"Folder_{count+1}"
        # os.makedirs(folder_name)
        A13toCPU1 = []
        B24toCPU2 = []
        CCto13 = []
        DCto24 = []
        for virtual_link in scenario:
            (VL, Source, Destination, Period, Exec_Time, Priority) = virtual_link
            VL = int(VL)
            Source = int(Source)
            Destination = int(Destination)
            Period = int(Period)
            Exec_Time = int(Exec_Time)
            Priority = int(Priority)
            # 13toCPU1.csv
            if Source == 1 or Source == 3:
                if Priority == 1:
                    A13toCPU1 = [[VL,Exec_Time,Period]] + A13toCPU1
                else:
                    A13toCPU1 = A13toCPU1 + [[VL,Exec_Time,Period]]
            # 24toCPU2.csv
            if Source == 2 or Source == 4:
                if Priority == 1:
                    B24toCPU2 = [[VL,Exec_Time,Period]] + B24toCPU2
                else:
                    B24toCPU2 = B24toCPU2 + [[VL,Exec_Time,Period]]
            # Cto13.csv
            if (Source == 2 or Source == 4) and (Destination == 1 or Destination == 3):
                if Priority == 1:
                    CCto13 = [[VL,Exec_Time,Period]] + CCto13
                else:
                    CCto13 = CCto13 + [[VL,Exec_Time,Period]]
            # Cto24.csv
            if (Source == 1 or Source == 3) and (Destination == 2 or Destination == 4):
                if Priority == 1:
                    DCto24 = [[VL,Exec_Time,Period]] + DCto24
                else:
                    DCto24 = DCto24 + [[VL,Exec_Time,Period]]
        for j in range(4):
            if j == 0:
                file_name = "A13toCPU1.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in A13toCPU1:
                        writer.writerow(line)
            elif j == 1:
                file_name = "B24toCPU2.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in B24toCPU2:
                        writer.writerow(line)
            elif j == 2:
                file_name = "CCto13.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in CCto13:
                        writer.writerow(line)
            elif j == 3:
                file_name = "DCto24.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in DCto24:
                        writer.writerow(line)
        count += 1
                    










       


