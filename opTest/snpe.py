#  @Time    : 2021/9/6 下午12:20
#  @Author  : lixiang
#  @FileName: snpe.py
#
import os
import re
import shutil
import subprocess

import adbutils


def prepare(client: adbutils.AdbDevice):
    client.shell("rm -rf /data/local/tmp/*.dlc")
    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/../SNPE/* /data/local/tmp/", stderr=subprocess.STDOUT,
                       shell=True))
    print(
        subprocess.run(f"adb  -s {client.serial} push {os.getcwd()}/../Convertors/snpe_models/* /data/local/tmp/", stderr=subprocess.STDOUT,
                       shell=True))
    client.shell("chmod 0777 /data/local/tmp/snpe-net-run")


def run(client: adbutils.AdbDevice):
    # try:
    #     os.mkdir("adbLogs/cpuLogs/snpe")
    # except:
    #     pass
    # subprocess.run("rm -rf adbLogs/snpe/*",shell=True)
    # model_name = 'mobilenet_v2'
    shutil.rmtree("./adbLogs/snpe/")
    os.makedirs("./adbLogs/snpe/cpu")
    os.makedirs("./adbLogs/snpe/info")
    os.makedirs("./adbLogs/snpe/snpe")
    shutil.rmtree("./csv/snpe/")
    os.mkdir("./csv/snpe/")
    for model_name in ['inception_v3.dlc','inception_v4.dlc',"mobilenet_v1.dlc","mobilenet_v2.dlc",'vgg.dlc']:
        input_list='target_l.txt'
        if 'inception' in model_name:
            input_list='target_raw_list.txt'
        out=client.shell(
            f"export LD_LIBRARY_PATH=/data/local/tmp &&cd /data/local/tmp&&/data/local/tmp/snpe-net-run --container {model_name} --input_list {input_list} --output_dir output_cpu")
        print(out)
        print(subprocess.run(
            f"adb  -s {client.serial} pull /data/local/tmp/output_cpu/SNPEDiag_0.log {os.getcwd()}/adbLogs/snpe/cpu/{model_name}.log",
            stderr=subprocess.STDOUT,
            shell=True))

        client.shell("rm -rf /data/local/tmp/output_gpu/*")
        client.shell("rm -rf /data/local/tmp/output_cpu/*")


def analyse():

    for files in os.listdir("adbLogs/snpe/cpu"):
        if '.log' in files:
            try:
                res_cpu = open("adbLogs/snpe/snpe/" + files, 'w+')
                # print(subprocess.check_output("cd snpe &&ls",
                #                                shell=True).decode('utf-8'))
                logs = subprocess.check_output("cd snpe && ./snpe-diagview --input_log ../adbLogs/snpe/cpu/" + files,
                                               shell=True).decode('utf-8')

                print(logs, file=res_cpu)
            except subprocess.CalledProcessError as e:
                print(e.output)
    for files in ['inception_v3.dlc','inception_v4.dlc',"mobilenet_v1.dlc","mobilenet_v2.dlc",'vgg.dlc']:
        if '.dlc' in files:
            try:
                res_cpu = open("adbLogs/snpe/info/" + files + ".log", 'w+')
                logs = subprocess.check_output("cd snpe && ./snpe-dlc-info -i  ../../Convertors/snpe_models/" + files, shell=True).decode('utf-8')

                print(logs, file=res_cpu)
            except subprocess.CalledProcessError as e:
                print(e.output)

    for files in os.listdir("adbLogs/snpe/info"):

        if '.log' in files:
            if '.info' in files:
                continue
            res_cpu = open("csv/snpe/"+files + ".info.csv", 'w+')
            res = open('adbLogs/snpe/snpe/' + files)
            infos = []
            for line in open("adbLogs/snpe/info/"+files).readlines():
                if '|' not in line:
                    continue
                typs = re.findall(r"\|\s*(\d+)\s*\|\s*(\S+)\s*\|", line)
                if len(typs) > 0:
                    print(typs)
                    infos.append(typs[0])
            i = 0
            for line in res.readlines():
                if ': CPU' not in line:
                    continue

                typs = re.findall(r"(\d+):\s+(.+)\s+: CPU", line)
                if len(typs) > 0:
                    print(typs)
                    timestr = int(typs[0][1].split(' ')[0])
                    infos[i] = infos[i] + (timestr / 1000,)

                    print(f"{infos[i][0]}\t{infos[i][1]}\t{infos[i][2]}", file=res_cpu)
                    i += 1





if __name__ == '__main__':
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    for d in adb.devices():
        print(d.serial)
    d = adb.device()
    prepare(d)
    run(d)
    analyse()