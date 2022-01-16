#  @Time    : 2021/9/6 下午6:51
#  @Author  : lixiang
#  @FileName: MNN.py
#
import os
import re
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm /data/local/tmp/MNN_models/*.mnn")
    print(subprocess.run(f"adb  -s  {client.serial} push {os.getcwd()}/../MNN/* /data/local/tmp/", stderr=subprocess.STDOUT,
                         shell=True))
    client.shell("chmod 0777 /data/local/tmp/benchmark.out&&mkdir /data/local/tmp/MNN_models")

    print(subprocess.run(f"adb  -s  {client.serial} push {os.getcwd()}/mnn/* /data/local/tmp/MNN_models",
                         stderr=subprocess.STDOUT, shell=True))


def run(client: adbutils.AdbDevice):
    models=['inception-v3.mnn','mobilenet-v1-1.0.mnn','mobilenet_v2.mnn','vgg16.mnn','resnet50.mnn']
    #./benchmark.out models_folder loop_count warm_up_count forwardtype
    logs=client.shell("export LD_LIBRARY_PATH=/data/local/tmp/ &&/data/local/tmp/benchmark.out /data/local/tmp/MNN_models 1 5 0")
    with open(f"adbLogs/mnn/CPU.log", 'w+') as f:
        f.write(logs)

def analyse():
    res = open("adbLogs/results/mnn/mnn.csv" , 'w+')
    for files in os.listdir("adbLogs/mnn"):
        if '.log' in files:
            log_file=open("adbLogs/mnn/"+files)
            res_name=files.replace(".log", "")
            for line in log_file.readlines():
                if line.startswith("Forward type:"):
                    types = re.findall(r"Forward type:\s*\*\*(.+?)\*\*", line)[0]
                    print(types)
                if line.startswith('[ - ] '):
                    name = re.findall(r"\[ - ]\s*(.+?)\s", line)[0]
                    print(name)
                    avg = re.findall(r"avg =\s*(.+?)\s", line)[0]
                    print(avg)
                    print(f"{name}\t{avg}\t{res_name}",file=res)



if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)



