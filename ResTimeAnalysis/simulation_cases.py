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
        os.makedirs(folder_name)
        A1toA = []
        B3toA = []
        C2toB = []
        D4toB = []
        EBtoA = []
        RFBtoA = []
        GAto1 = []
        HAto3 = []
        IBto2 = []
        JBto4 = []
        

        for virtual_link in scenario:
            (VL, Source, Destination, Period, Exec_Time, Priority) = virtual_link
            VL = int(VL)
            Source = int(Source)
            Destination = int(Destination)
            Period = int(Period)
            Exec_Time = int(Exec_Time)
            Priority = int(Priority)
            if Source == 1:
                if Priority == 1:
                    A1toA = [[VL,Exec_Time,Period]] + A1toA
                else:
                    A1toA = A1toA + [[VL,Exec_Time,Period]]
            if Source == 2:
                if Priority == 1:
                    B3toA = [[VL,Exec_Time,Period]] + B3toA
                else:
                    B3toA = B3toA + [[VL,Exec_Time,Period]]
            if Source == 3:
                if Priority == 1:
                    C2toB = [[VL,Exec_Time,Period]] + C2toB
                else:
                    C2toB = C2toB + [[VL,Exec_Time,Period]]
            if Source == 4:
                if Priority == 1:
                    D4toB = [[VL,Exec_Time,Period]] + D4toB
                else:
                    D4toB = D4toB + [[VL,Exec_Time,Period]]
            if Destination == 1:
                if Priority == 1:
                    GAto1 = [[VL,Exec_Time,Period]] + GAto1
                else:
                    GAto1 = GAto1 + [[VL,Exec_Time,Period]]
            if Destination == 3:
                if Priority == 1:
                    HAto3 = [[VL,Exec_Time,Period]] + HAto3
                else:
                    HAto3 = HAto3 + [[VL,Exec_Time,Period]]
            if ((Source == 1) or (Source == 3)) and ((Destination == 2) or (Destination == 4)):
                if Priority == 1:
                    RFBtoA = [[VL,Exec_Time,Period]] + RFBtoA
                else:
                    RFBtoA = RFBtoA + [[VL,Exec_Time,Period]]
            if Destination == 2:
                if Priority == 1:
                    IBto2 = [[VL,Exec_Time,Period]] + IBto2
                else:
                    IBto2 = IBto2 + [[VL,Exec_Time,Period]]
            if Destination == 4:
                if Priority == 1:
                    JBto4 = [[VL,Exec_Time,Period]] + JBto4
                else:
                    JBto4 = JBto4 + [[VL,Exec_Time,Period]]
            if ((Source == 2) or (Source == 4)) and ((Destination == 1) or (Destination == 3)):
                if Priority == 1:
                    EBtoA = [[VL,Exec_Time,Period]] + EBtoA
                else:
                    EBtoA = EBtoA + [[VL,Exec_Time,Period]]
        for j in range(10):
            if j == 0:
                file_name = "A1toA.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in A1toA:
                        writer.writerow(line)
            elif j == 1:
                file_name = "B3toA.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in B3toA:
                        writer.writerow(line)
            elif j == 2:
                file_name = "C2toB.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in C2toB:
                        writer.writerow(line)
            elif j == 3:
                file_name = "D4toB.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in D4toB:
                        writer.writerow(line)
            elif j == 4:
                file_name = "GAto1.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in GAto1:
                        writer.writerow(line)
            elif j == 9:
                file_name = "HAto3.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in HAto3:
                        writer.writerow(line)
            elif j == 6:
                file_name = "RFBtoA.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in RFBtoA:
                        writer.writerow(line)
            elif j == 7:
                file_name = "IBto2.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in IBto2:
                        writer.writerow(line)
            elif j == 8:
                file_name = "JBto4.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in JBto4:
                        writer.writerow(line)
            elif j == 5:
                file_name = "EBtoA.csv"
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["index","execution" "time(C)","Period(T)"])
                    for line in EBtoA:
                        writer.writerow(line)
        count += 1
                    










       


