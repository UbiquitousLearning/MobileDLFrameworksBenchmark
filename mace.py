#  @Time    : 2021/9/6 下午7:38
#  @Author  : lixiang
#  @FileName: mace.py
#
import os
import re
import shutil
import subprocess

import adbutils


def prepare():
    pass


def run():
    # model_name='inception_v3'
    # print(subprocess.run(f"cd adbLogs/mace &&rm -rf * &&mkdir err"))
    shutil.rmtree("adbLogs/mace/")
    os.makedirs("adbLogs/mace/err")
    try:
        os.mkdir("adbLogs/cpuLogs/mace")
    except:
        pass
    subprocess.run("rm -rf adbLogs/cpuLogs/mace/*",shell=True)

    for model_name in os.listdir("./Convertors/MACE_models/CPU"):
        if not model_name.endswith(".yaml"):
            continue
        try:
            frequency_monitor = subprocess.Popen(
                f'adb shell "top -d 0.01" |grep mace_run  >./adbLogs/cpuLogs/mace/{model_name}.cpu.log',
                shell=True)
            log = subprocess.check_output(
                f"cd Convertors/mace-master &&python3 tools/python/run_model.py --config ../MACE_models/CPU/{model_name} --benchmark --runtime=cpu --vlog_level=2",
                shell=True)
            frequency_monitor.kill()
            with open("adbLogs/mace/" + model_name + '_cpu.log', 'wb+') as f:
                f.write(log)
        except subprocess.CalledProcessError as e:
            with open("adbLogs/mace/err/" + model_name + '_cpu.log', 'wb+') as f:
                f.write(e.output)
            print(e.output)
            print(e.stdout)
            print(e.stderr)
    for model_name in os.listdir("./Convertors/MACE_models/GPU"):
        if not model_name.endswith(".yaml"):
            continue
        try:
            frequency_monitor = subprocess.Popen(
                f'adb shell "top -d 0.01" |grep mace_run  >./adbLogs/cpuLogs/mace/{model_name}.gpu.log',
                shell=True)
            log = subprocess.check_output(
                f"cd Convertors/mace-master &&python3 tools/python/run_model.py --config ../MACE_models/GPU/{model_name} --benchmark --runtime=gpu --vlog_level=2",
                shell=True)
            frequency_monitor.kill()

            with open("adbLogs/mace/" + model_name + '_gpu.log', 'wb+') as f:
                f.write(log)
        except subprocess.CalledProcessError as e:
            print(e.output)
            with open("adbLogs/mace/err/" + model_name + '_gpu.log', 'wb+') as f:
                f.write(e.output)
            print(e.stdout)
            print(e.stderr)


def analyse():
    res_cpu = open("adbLogs/results/mace/mace_cpu.csv", 'w+')
    res_gpu = open("adbLogs/results/mace/mace_gpu.csv", 'w+')
    print("ModelName\twarmup\trun_avg", file=res_gpu)
    print("ModelName\twarmup\trun_avg", file=res_cpu)
    for files in os.listdir("adbLogs/mace"):
        if '.log' in files:
            if 'cpu' in files:
                res = res_cpu
            elif 'gpu' in files:
                res = res_gpu
            else:
                continue
            print(files)
            log_file = open("adbLogs/mace/" + files)
            res_name = files.replace(".log", "")
            for line in log_file.readlines():
                if line.startswith("time"):
                    print(line)
                    types = re.findall(r"time\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+", line)[0]
                    print(types)
                    print(f"{res_name}\t{types[2]}\t{types[3]}", file=res)


if __name__ == '__main__':
    # prepare()
    # run()
    analyse()
