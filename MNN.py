#  @Time    : 2021/9/6 下午6:51
#  @Author  : lixiang
#  @FileName: MNN.py
#
import os
import re
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm /data/local/tmp/*.mnn")
    print(subprocess.run(f"adb  -s  {client.serial} push {os.getcwd()}/MNN/* /data/local/tmp/", stderr=subprocess.STDOUT,
                         shell=True))
    client.shell("chmod 0777 /data/local/tmp/benchmark.out&&mkdir /data/local/tmp/MNN_models")

    print(subprocess.run(f"adb  -s  {client.serial} push {os.getcwd()}/Convertors/MNN_models/* /data/local/tmp/MNN_models",
                         stderr=subprocess.STDOUT, shell=True))


def run(client: adbutils.AdbDevice):
    try:
        os.mkdir("adbLogs/cpuLogs/mnn")
    except:
        pass
    # frequency_monitor = subprocess.Popen('adb shell "top -d 1"|grep benchmark.out >adbLogs/cpuLogs/mnn/cpu.log',
    #                                          shell=True)
    # logs=client.shell("export LD_LIBRARY_PATH=/data/local/tmp/ &&/data/local/tmp/benchmark.out /data/local/tmp/MNN_models 50 5 0")
    # frequency_monitor.kill()
    # with open(f"adbLogs/mnn/CPU.log", 'w+') as f:
    #     f.write(logs)
    # frequency_monitor = subprocess.Popen('adb shell "top -d 1"|grep benchmark.out >adbLogs/cpuLogs/mnn/Vulkan.log',
    #                                          shell=True)
    # logs=client.shell("export LD_LIBRARY_PATH=/data/local/tmp/ &&/data/local/tmp/benchmark.out /data/local/tmp/MNN_models 50 5 7")
    # frequency_monitor.kill()
    # with open(f"adbLogs/mnn/Vulkan.log", 'w+') as f:
    #     f.write(logs)
    # frequency_monitor = subprocess.Popen('adb shell "top -d 1"|grep benchmark.out >adbLogs/cpuLogs/mnn/OpenGL.log',
    #                                          shell=True)

    logs=client.shell("export LD_LIBRARY_PATH=/data/local/tmp/ &&/data/local/tmp/benchmark.out /data/local/tmp/MNN_models 50 5 3")
    # frequency_monitor.kill()
    with open(f"adbLogs/mnn/OpenCL.log", 'w+') as f:
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
                if  'avg =' in line and '[ - ]' in line:
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
    analyse()



