# load raw data and extract their attributes into csv file
import os

import pandas as pd
import sys
import numpy as np


path_to_freq = "adbLogs/tensorflow/"

def prase_temperature(path_to_freq: str) -> tuple:
    raw_data = pd.read_table(path_to_freq, header=None, sep=",", engine='python')

    attributes = ["stamp", "temperature", "cpu0", "cpu1", "cpu2", "cpu3", "cpu4", "cpu5", "cpu6", "cpu7","SOC"]
    processed_data = pd.DataFrame(index=attributes)

    data = pd.Series(["nan"] * 11, attributes)

    start_time = int(raw_data[0][1].split()[2])

    count = 0
    for line in raw_data[0]:
        if "NEW DATA" in line:
            count = count + 1
            data["stamp"] = int(line.split()[2]) - start_time
        if "temperature" in line:
            temp_loc = line.split(" ").index("temperature:")
            # data["temperature"] = 1
            data["temperature"] = float(line.split(" ")[temp_loc + 1])
        for attribute in attributes[2:]:
            if attribute in line:
                data[attribute] = float(line.split()[1])
        if "END" in line:
            processed_data[count] = data
            data[:] = "nan"

    matrix = processed_data.T
    matrix.to_csv(path_to_freq.replace(".result",".csv"))
    # print(matrix)


for files in os.listdir(path_to_freq):
    if not os.path.isdir(path_to_freq+files) and ".result" in files:
        prase_temperature(path_to_freq+files)


