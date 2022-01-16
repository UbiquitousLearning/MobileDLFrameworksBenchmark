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
import shutil
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    # subprocess.run(f'rm  {os.getcwd()}/csv/ncnn/*')
    shutil.rmtree("./adbLogs/ncnn/")
    os.mkdir("./adbLogs/ncnn/")
    shutil.rmtree("./csv/ncnn/")
    os.mkdir("./csv/ncnn/")


    # subprocess.run(f'rm -rf {os.getcwd()}/adbLogs/ncnn/*')
    client.shell("rm /data/local/tmp/*.param")

    print(subprocess.run(f"adb -s {client.serial} push  {os.getcwd()}/ncnn/benchncnn /data/local/tmp/",
                         stderr=subprocess.STDOUT,
                         shell=True))
    client.shell("chmod 0777 /data/local/tmp/benchncnn")
    print(subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/../Convertors/ncnn_models/* /data/local/tmp",
                         stderr=subprocess.STDOUT, shell=True))


def run(client: adbutils.AdbDevice):
    # CPU
    log_filename = "adbLogs/ncnn/cpu.log"
    logs = client.shell(
        "cd /data/local/tmp/ &&chmod 777 benchncnn &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchncnn 4 4")
    with open(log_filename, 'w+') as f:
        f.write(logs)
    # # GPU
    # log_filename = "adbLogs/ncnn/gpu.log"
    # logs = client.shell(
    #     "cd /data/local/tmp/ &&chmod 777 benchncnn &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchncnn 4 8 0 0 1")
    # with open(log_filename, 'w+') as f:
    #     f.write(logs)


def analyse():
    content = ''
    # 预热8次 运行4次
    NUMBER = 12
    number = 0
    for line in open("adbLogs/ncnn/cpu.log").readlines():
        if 'avg = ' in line:
            name = re.findall(r'^\s+(\S+)\s+min', line)[0]

            with open(f'csv/ncnn/{name}.log', 'w+') as f:
                content += line
                print(content, file=f)
                content = ''
                number = 0
        else:
            if '|' in line:
                if number >= NUMBER - 1 and not line.startswith("Split"):
                    # Split层一般没有时间 也没啥用 去掉不统计
                    # number>=NUMBER-1统计最后一次的
                    stat = re.findall(r'^(\S+)\s+\S+\s+(\S+)\s+\|', line)[0]
                    content += f"{stat[0]}\t{stat[1]}\n"
                if line.startswith("Softmax"):
                    number += 1


if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    analyse()
