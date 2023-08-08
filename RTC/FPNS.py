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

# parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_output', type=str, required=True)
    args = parser.parse_args()
    return args

def read_input_file(file_path):
    data_frames = pd.read_csv(file_path)
    doc = data_frames.values
    return doc

def compute_recurrent(maxC, i, I_curr, I_prev, execution_list, period_list, count):
    if I_curr == I_prev and (count != 0):
        return I_curr
    else:
        summation = 0
        if i != 0:
            summation =  np.sum(np.dot(np.int_(I_curr/period_list[:i])+1,execution_list[:i]))
        I_prev = I_curr
        I_curr = maxC+summation
        return compute_recurrent(maxC, i, I_curr, I_prev, execution_list, period_list, count+1)

def worst_case_compute(index_list, execution_list, period_list):
    result = np.zeros(len(index_list))
    print(index_list[:(len(index_list)-1)])
    for i in range(len(index_list)-1):
        maxC = max(execution_list[(i+1):])
        I = execution_list[i]+compute_recurrent(maxC, i, 0, 0, execution_list, period_list, 0)
        result[i] = I
    result[-1] = 1
    return result

def process_input_files(folder_path, writer):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename[0] != 't':
            file_path = os.path.join(folder_path, filename)
            print(f"Calculating the worst case delay of this architecture: {file_path}. ")
            streams = read_input_file(file_path)
            index_list = streams[:,0]
            execution_list = streams[:,1]
            period_list = streams[:,2]
            result_list = worst_case_compute(index_list, execution_list, period_list)
            for i in range(len(result_list)):
                print(f"stream index: {index_list[i]}, worst case delay: {result_list[i]}")
                writer.writerow([index_list[i],result_list[i]])
            
                
if __name__ == "__main__":
    args = parse_args()
    folder_path = "FPNS_small_test"
    dic={}
    with open(args.csv_output, 'w') as result: 
        writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        process_input_files(folder_path, writer)
    with open(args.csv_output, 'r') as result: 
        reader = csv.reader(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] in dic:
                dic[row[0]] += float(row[1])
            else:
                dic[row[0]] = float(row[1])
    print(dic)


