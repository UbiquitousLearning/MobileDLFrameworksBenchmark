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
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm /data/local/tmp/*.tflite")

    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/tensorflow/latest/benchmark_model /data/local/tmp/",
                       stderr=subprocess.STDOUT,
                       shell=True))
    client.shell("chmod 777 /data/local/tmp/benchmark_model &&chmod +x /data/local/tmp/benchmark_model")
    print(subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/Convertors/tflite_models/* /data/local/tmp/",
                         stderr=subprocess.STDOUT,
                         shell=True))


def run(client: adbutils.AdbDevice):
    # model_name = "mobilenet_quant_v1_224"
    try:
        os.mkdir("adbLogs/cpuLogs/tflite")
    except:
        pass
    # subprocess.run("rm -rf adbLogs/cpuLogs/tflite/*",shell=True)
    for model_name in os.listdir("./Convertors/tflite_models"):
        frequency_monitor = subprocess.Popen(
            f'adb shell "sleep 0.1 && top -d 0.01"|grep benchmark_mod  >adbLogs/cpuLogs/tflite/{model_name}.cpu.log',
            shell=True)
        log = client.shell(
            f"cd /data/local/tmp/ &&chmod +x benchmark_model &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchmark_model --graph={model_name}  --num_threads=4")
        frequency_monitor.kill()
        with open(f"adbLogs/tflite/{model_name}_cpu.log", 'w+') as f:
            f.write(log)
        # frequency_monitor = subprocess.Popen(
        #     f'adb shell "top -d 0.01"|grep snpe|grep -v grep >adbLogs/cpuLogs/tflite/{model_name}.gpu.log',
        #     shell=True)
        # log = client.shell(
        #     f"cd /data/local/tmp/ &&chmod +x benchmark_model &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchmark_model --graph={model_name} --num_threads=8 --use_gpu=true")
        # frequency_monitor.kill()
        # with open(f"adbLogs/tflite/{model_name}_gpu.log", 'w+') as f:
        #     f.write(log)


def analyse():
    res_cpu = open("adbLogs/results/tflite/tflite_cpu.csv", 'w+')
    res_gpu = open("adbLogs/results/tflite/tflite_gpu.csv", 'w+')

    print("name\twarmup\tavg", file=res_cpu)
    print("name\twarmup\tavg", file=res_gpu)

    for files in os.listdir("adbLogs/tflite"):
        if '.log' in files:
            log_file = open("adbLogs/tflite/" + files)
            if '.log' in files:
                if 'cpu' in files:
                    res = res_cpu
                elif 'gpu' in files:
                    res = res_gpu
                else:
                    continue
            file_name = files.replace(".log", "")
            for line in log_file.readlines():
                if "Average inference timings in us:" in line:
                    avg = 0
                    if 'no stats' in line:
                        avg = re.findall(r"no stats:\s*(.+)", line)[0]
                        print(avg)
                    if 'Inference:' in line:
                        avg = re.findall(r"Inference:\s*(.+)", line)[0]
                        print(avg)
                    print(f"{file_name}\t{avg}", file=res)
                elif 'Inference timings in us:' in line:
                    avg = re.findall(r"Inference \(avg\):\s*(.+)", line)[0]
                    warmup = re.findall(r"Warmup \(avg\):\s*(.+?),", line)[0]

                    print(avg)
                    print(f"{file_name}\t{warmup}\t{avg}", file=res)


if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    analyse()
