#  @Time    : 2021/8/1
#  @Author  : lixiang
#  @FileName: prase_log_ncnn.py


import os
import re

Model_Name='mobilenet'
file=open("ncnn.csv","w+")
print("Date\tAvg\tVulkan",file=file)
for files in os.listdir("adbLogs/ncnn"):
    if not os.path.isdir("adbLogs/ncnn"+files) and ".log" in files:
        print(files)
        file_name=files.replace(".log","").split("_")
        if len(file_name)<2:
            continue
        file_name=file_name[2]
        flag=0
        if 'v' in files:
            flag=1
        with open(files) as f:
            content=f.readlines()

        for line in content:
            if Model_Name+" " in line:
                avg=re.findall(r"avg =\s*(.+)",line)[0]
                print(avg)
                print(f"{file_name}\t{avg}\t{flag}",file=file)

