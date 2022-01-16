#  @Time    : 2021/9/8 下午9:17
#  @Author  : lixiang
#  @FileName: ncnn.py
#

#  @Time    : 2021/9/8 下午4:39
#  @Author  : lixiang
#  @FileName: ncnn.py
#
import os
import re
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm /data/local/tmp/*.param")

    print(subprocess.run(f"adb -s {client.serial} push  {os.getcwd()}/ncnn/benchncnn /data/local/tmp/",
                         stderr=subprocess.STDOUT,
                         shell=True))
    client.shell("chmod 0777 /data/local/tmp/benchncnn")
    print(subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/../Convertors/ncnn_models/* /data/local/tmp",
                         stderr=subprocess.STDOUT, shell=True))


def run(client: adbutils.AdbDevice):
    try:
        os.makedirs("../adbLogs/cpuLogs/ncnn/")
    except:
        pass
    # CPU
    for filename,model_size in [('inception_v3','395,395,3'),('inception_v4','299,299,3'),('vgg16','224,224,3'),('mnasnet','224,224,3'),('mobilenet','224,224,3'),('mobilenet_v2','224,224,3'),('squeezenet','229,227,3')]:
        log_filename = f"../adbLogs/ncnn/{filename}.log"
        frequency_monitor = subprocess.Popen(f'sleep 0.1 && adb shell "top -d 0.01"|grep benchncnn >../adbLogs/cpuLogs/ncnn/{filename}.cpu.log',
                                                 shell=True)
        logs = client.shell(
            f"cd /data/local/tmp/ &&chmod 777 benchncnn &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchncnn {filename} {model_size} 30 4")
        frequency_monitor.kill()
        with open(log_filename, 'w+') as f:
            f.write(logs)

    # GPU
    # log_filename = "adbLogs/ncnn/gpu.log"
    # frequency_monitor = subprocess.Popen('sleep 1 && adb shell "top -d 1"|grep benchmark.out|grep -v grep >adbLogs/cpuLogs/ncnn/gpu.log',
    #                                          shell=True)
    # logs = client.shell(
    #     "cd /data/local/tmp/ &&chmod 777 benchncnn &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchncnn 4 4 0 0 1")
    # frequency_monitor.kill()
    #     with open(log_filename, 'w+') as f:
    #         f.write(logs)


def analyse():
    res_cpu = open("adbLogs/results/ncnn/ncnn_cpu.csv", 'w+')
    res_gpu = open("adbLogs/results/ncnn/ncnn_gpu.csv", 'w+')

    print("name\tmin\tmax\tavg", file=res_cpu)
    print("name\tmin\tmax\tavg", file=res_gpu)

    for files in os.listdir("adbLogs/ncnn"):
        if '.log' in files:
            log_file = open("adbLogs/ncnn/" + files)
            if '.log' in files:
                if 'cpu' in files:
                    res = res_cpu
                elif 'gpu' in files:
                    res = res_gpu
                else:
                    continue
            # res_name=files.replace(".log", ".csv")
            for line in log_file.readlines()[3:]:
                print(line)
                types = re.findall(r"\s*(.+?)\s*min =\s*(.+?)\s+max =\s+(.+?)\s+avg =\s+(.+)\s*", line)
                if len(types) > 0:
                    stats = types[0]
                    print("\t".join(stats), file=res)


if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    # analyse()
