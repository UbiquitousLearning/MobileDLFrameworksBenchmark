#  @Time    : 2021/9/8 下午9:17
#  @Author  : lixiang
#  @FileName: tflite.py
#

#  @Time    : 2021/9/8 下午7:53
#  @Author  : lixiang
#  @FileName: tflite.py
#
import os
import re
import shutil
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm /data/local/tmp/*.tflite")
    shutil.rmtree("./adbLogs/tflite/")
    os.mkdir("./adbLogs/tflite/")
    shutil.rmtree("./csv/tflite/")
    os.mkdir("./csv/tflite/")

    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/../tensorflow/latest/benchmark_model /data/local/tmp/",
                       stderr=subprocess.STDOUT,
                       shell=True))
    client.shell("chmod 777 /data/local/tmp/benchmark_model &&chmod +x /data/local/tmp/benchmark_model")
    print(subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/tflite/* /data/local/tmp/",
                         stderr=subprocess.STDOUT,
                         shell=True))


def run(client: adbutils.AdbDevice):
    # model_name = "mobilenet_quant_v1_224"
    for model_name in os.listdir("./tflite"):
        log = client.shell(
            f"cd /data/local/tmp/ &&chmod +x benchmark_model &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchmark_model --graph={model_name} --num_threads=4 --enable_op_profiling=true")
        with open(f"adbLogs/tflite/{model_name}_cpu.log", 'w+') as f:
            f.write(log)
        # log = client.shell(
        #     f"cd /data/local/tmp/ &&chmod +x benchmark_model &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchmark_model --graph={model_name} --num_threads=8 --use_gpu=true --enable_op_profiling=true")
        # with open(f"adbLogs/tflite/{model_name}_gpu.log", 'w+') as f:
        #     f.write(log)


def analyse():
    for files in os.listdir("adbLogs/tflite"):

        if '.log' in files:
            if '.info' in files:
                continue
            res_cpu = open("csv/tflite/"+files + ".log", 'w+')
            flag=0
            for line in open("adbLogs/tflite/"+files).readlines():
                if "Operator-wise Profiling Info for Regular Benchmark Runs:" in line:
                    flag=1
                if flag==0:
                    continue
                typs = re.findall(r"^\s*(\S+)\s+\S+\s+\s+\S+\s+(\S+)\s*", line)
                if len(typs) > 0:
                    print(f'{typs[0][0]}\t{typs[0][1]}', file=res_cpu)



if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    # prepare(d)
    # run(d)
    analyse()
