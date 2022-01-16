#  @Time    : 2021/9/9 上午9:26
#  @Author  : lixiang
#  @FileName: pytorchm.py
#
import os
import re
import shutil
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/pytorchM/speed_benchmark_torch /data/local/tmp/",
                       stderr=subprocess.STDOUT,
                       shell=True))
    client.shell("chmod 777 /data/local/tmp/speed_benchmark_torch &&chmod +x /data/local/tmp/speed_benchmark_torch")
    print(subprocess.run(f"adb -s {client.serial} push {os.getcwd()}/Convertors/torch_models/* /data/local/tmp/",
                         stderr=subprocess.STDOUT,
                         shell=True))


def run(client: adbutils.AdbDevice):
    try:
        shutil.rmtree("./adbLogs/cpuLogs/torch/")
    except Exception as e:
        print(e)
        pass
    os.mkdir("./adbLogs/cpuLogs/torch/")

    # model_name = "mobilenet_quant_v1_224"
    for model_name in os.listdir("./Convertors/torch_models"):

        input_type=model_name.split(".")[0].split("_")[-1]
        frequency_monitor = subprocess.Popen(f'sleep 0.1 &adb shell "top -d 0.01"|grep speed_bench >adbLogs/cpuLogs/torch/{model_name}.log',
                                                 shell=True)
        log = client.shell(
            f'cd /data/local/tmp/ &&chmod +x speed_benchmark_torch &&export LD_LIBRARY_PATH=/data/local/tmp &&./speed_benchmark_torch --iter 30  --model=/data/local/tmp/{model_name} --input_dims="{input_type}" --input_type="float"')
        frequency_monitor.kill()
        with open(f"adbLogs/torch/{model_name}_cpu.log", 'w+') as f:
            f.write(log)



def analyse():
    res_cpu = open("adbLogs/results/torch/torch_cpu.csv", 'w+')
    res_gpu = open("adbLogs/results/torch/torch_gpu.csv", 'w+')

    print("name\tavg", file=res_cpu)
    print("name\tavg", file=res_gpu)

    for files in os.listdir("adbLogs/torch"):
        if '.log' in files:
            log_file = open("adbLogs/torch/" + files)
            if '.log' in files:
                if 'cpu' in files:
                    res = res_cpu
                elif 'gpu' in files:
                    res = res_gpu
                else:
                    continue
                file_name = files.replace(".log", "").replace("_cpu","").replace("_gpu","")
                for line in log_file.readlines():
                    if "Microseconds per iter:" in line:
                        # print(line)

                        avg = re.findall(r"Microseconds per iter:\s+(.+?).\s+",line)
                        # print(avg)
                        if(len(avg))>0:
                            print(f"{file_name}\t{avg[0]}", file=res)
if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    analyse()