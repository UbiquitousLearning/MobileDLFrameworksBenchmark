#  @Time    : 2021/9/6 下午12:20
#  @Author  : lixiang
#  @FileName: snpe.py
#
import os
import re
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm -rf /data/local/tmp/*.dlc")
    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/SNPE/* /data/local/tmp/", stderr=subprocess.STDOUT,
                       shell=True))
    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/Convertors/snpe_models/* /data/local/tmp/", stderr=subprocess.STDOUT,
                       shell=True))
    client.shell("chmod 0777 /data/local/tmp/snpe-net-run")


def run(client: adbutils.AdbDevice):
    try:
        os.mkdir("adbLogs/cpuLogs/snpe")
    except:
        pass
    subprocess.run("rm -rf adbLogs/cpuLogs/snpe/*",shell=True)
    # model_name = 'mobilenet_v2'
    for model_name in os.listdir("Convertors/snpe_models"):
        input_list='target_l.txt'
        if 'inception' in model_name:
            input_list='target_raw_list.txt'
        frequency_monitor = subprocess.Popen(
            f'adb shell "top -d 0.01"|grep snpe|grep -v grep >adbLogs/cpuLogs/snpe/{model_name}.cpu.log',
            shell=True)
        client.shell(
            f"export LD_LIBRARY_PATH=/data/local/tmp &&cd /data/local/tmp&&/data/local/tmp/snpe-net-run --container {model_name} --input_list {input_list} --output_dir output_cpu --perf_profile high_performance --profiling_level basic")
        frequency_monitor.kill()
        print(subprocess.run(
            f"adb  -s {client.serial} pull /data/local/tmp/output_cpu/SNPEDiag_0.log {os.getcwd()}/adbLogs/snpe/cpu/{model_name}.log",
            stderr=subprocess.STDOUT,
            shell=True))
        frequency_monitor = subprocess.Popen(
            f'adb shell "top -d 0.01"|grep snpe|grep -v grep >adbLogs/cpuLogs/snpe/{model_name}.gpu.log',
            shell=True)
        print(client.shell(
            f"export LD_LIBRARY_PATH=/data/local/tmp &&cd /data/local/tmp&&/data/local/tmp/snpe-net-run --container {model_name} --input_list {input_list}  --output_dir output_gpu --use_gpu --perf_profile high_performance --profiling_level basic")
        )
        frequency_monitor.kill()
        print(subprocess.run(
            f"adb  -s {client.serial} pull /data/local/tmp/output_gpu/SNPEDiag_0.log {os.getcwd()}/adbLogs/snpe/gpu/{model_name}.log",
            stderr=subprocess.STDOUT,
            shell=True))
        client.shell("rm -rf /data/local/tmp/output_gpu/*")
        client.shell("rm -rf /data/local/tmp/output_cpu/*")


def analyse():
    res_cpu = open("adbLogs/results/snpe/snpe_cpu.csv", 'w+')
    res_gpu = open("adbLogs/results/snpe/snpe_gpu.csv", 'w+')

    print("name\tavg", file=res_cpu)
    print("name\tavg", file=res_gpu)
    for files in os.listdir("adbLogs/snpe/cpu"):
        if '.log' in files:
            logs = subprocess.check_output("./snpe-diagview --input_log ./adbLogs/snpe/cpu/" + files, shell=True).decode('utf-8')
            typs = re.findall(r"Total Inference Time:\s*(.+)\s+", logs)
            if len(typs) > 0:
                print(f"{files.replace('.log', '')}\t{typs[0]}", file=res_cpu)
    for files in os.listdir("adbLogs/snpe/gpu"):
        if '.log' in files:
            logs = subprocess.check_output("./snpe-diagview --input_log ./adbLogs/snpe/gpu/" + files, shell=True).decode('utf-8')
            typs = re.findall(r"Total Inference Time:\s*(.+)\s+", logs)
            if len(typs) > 0:
                print(f"{files.replace('.log', '')}\t{typs[0]}", file=res_gpu)

if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    # analyse()