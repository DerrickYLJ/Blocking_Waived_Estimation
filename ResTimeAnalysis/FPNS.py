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

stream_dictionary = { (i+1):set() for i in range(13)}
final_result = { (i+1):0 for i in range(13)}

# # parse arguments
# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--csv_output', type=str, required=True)
#     args = parser.parse_args()
#     return args

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
            summation =  np.sum(np.dot(np.int_(I_curr/period_list)+1,execution_list))
        I_prev = I_curr
        I_curr = maxC+summation
        return compute_recurrent(maxC, i, I_curr, I_prev, execution_list, period_list, count+1)

def worst_case_compute(index_list, execution_list, period_list):
    result = np.zeros(len(index_list))
    print(index_list[:(len(index_list)-1)])
    for i in range(len(index_list)):
        curr_index = index_list[i]
        input_executaion_list=[]
        input_period_list=[]
        # Start exclusing streams that have blocked before
        if i != 0:
            for j in range(i):
                if index_list[j] in stream_dictionary[curr_index]:
                    continue
                else:
                    input_executaion_list.append(execution_list[j])
                    input_period_list.append(period_list[j])
                    stream_dictionary[curr_index].add(index_list[j])
        if i != len(index_list)-1:
            maxC = max(execution_list[(i+1):])
        else:
            maxC = 0
        I = execution_list[i]+compute_recurrent(maxC, i, 0, 0, np.array(input_executaion_list), np.array(input_period_list), 0)
        result[i] = I
    # result[-1] = execution_list[-1]+compute_recurrent(0, len(index_list)-1, 0, 0, execution_list, period_list, 0)
    return result

def process_input_files(folder_path, writer):
    s = {'A','B','C','D', 'E', 'F'}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename[0] in s:
            file_path = os.path.join(folder_path, filename)
            print(f"Calculating the worst case delay of this architecture: {file_path}. ")
            with open(file_path, 'r') as file:
                first_line = file.readline()
                second_line = file.readline().strip()
                if not second_line:
                    continue
                streams = read_input_file(file_path)
                index_list = streams[:,0]
                print(streams)
                execution_list = streams[:,1]
                period_list = streams[:,2]
                result_list = worst_case_compute(index_list, execution_list, period_list)
                for i in range(len(result_list)):
                    print(f"stream index: {index_list[i]}, worst case delay: {result_list[i]}")
                    writer.writerow([index_list[i],result_list[i]])


def update_final_result(index, delay):
    final_result[index] = max(final_result[index], delay)
            
if __name__ == "__main__":
    for count in range(72):
        stream_dictionary = { (i+1):set() for i in range(13)}
        folder_path = f"Folder_{count+1}"
        file_name = f"File_{count+1}.csv"
        file_path = os.path.join(folder_path, file_name)
        dic={}
        with open(file_path, 'w') as result: 
            writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            process_input_files(folder_path, writer)
        with open(file_path, 'r') as result: 
            reader = csv.reader(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                key = int(row[0])
                if key in dic:
                    dic[key] += float(row[1])
                else:
                    dic[key] = float(row[1])
        myKeys = list(dic.keys())
        myKeys.sort()
        sorted_dict = [(key, dic[key]) for key in myKeys]
        # plt.plot([key for (key, value) in sorted_dict], [value for (key, value) in sorted_dict], "*-")
        # plt.plot([key for (key, value) in sorted_dict], [205, 235, 408, 310, 175, 197, 261, 245, 475, 362, 456, 203, 422], "o-")
        # plt.show()
        print(sorted_dict)
        for (key, value) in sorted_dict:
            update_final_result(key, value)
    # print out final result
    print("---------printing final worst case delay----------")
    mykeys = list(final_result.keys())
    mykeys.sort()
    sorted_dict = [(key, final_result[key]) for key in myKeys]
    print(sorted_dict)
    plt.plot([key for (key, value) in sorted_dict], [value for (key, value) in sorted_dict], "*-")
    plt.plot([key for (key, value) in sorted_dict], [205, 235, 408, 310, 175, 197, 404, 382, 618, 362, 580, 208, 422], "o-")
    plt.show()

