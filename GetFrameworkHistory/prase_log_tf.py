#  @Time    : 2021/8/1
#  @Author  : lixiang
#  @FileName: prase_log_tf.py


import os
import re

# Model_Name='mobilenet'
file=open("tf.csv","w+")
print("Date\tAvg",file=file)
for files in os.listdir("adbLogs/tensorflow"):
    if not os.path.isdir("adbLogs/tensorflow/"+files) and ".log" in files:
        print(files)
        file_name=files.replace(".log","").split("_")
        if len(file_name)<2:
            continue
        file_name=file_name[1]
        with open("adbLogs/tensorflow/"+files) as f:
            content=f.readlines()

        for line in content:
            if "Average inference timings in us:" in line:
                avg=0
                if 'no stats' in line:
                    avg=re.findall(r"no stats:\s*(.+)",line)[0]
                    print(avg)
                if 'Inference:' in line:
                    avg=re.findall(r"Inference:\s*(.+)",line)[0]
                    print(avg)
                print(f"{file_name}\t{avg}",file=file)
            elif 'Inference timings in us:' in line:
                avg=re.findall(r"Inference \(avg\):\s*(.+)",line)[0]
                print(avg)
                print(f"{file_name}\t{avg}",file=file)

