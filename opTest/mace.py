#  @Time    : 2021/10/12 下午5:09
#  @Author  : lixiang
#  @FileName: mace.py
#
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
    # try:
    #     os.mkdir("adbLogs/cpuLogs/mace")
    # except:
    #     pass
    # subprocess.run("rm -rf adbLogs/cpuLogs/mace/*",shell=True)

    for model_name in os.listdir("./mace"):
        if not model_name.endswith(".yaml"):
            continue
        try:
            # frequency_monitor = subprocess.Popen(
            #     f'adb shell "top -d 0.01" |grep mace_run  >./adbLogs/cpuLogs/mace/{model_name}.cpu.log',
            #     shell=True)
            log = subprocess.check_output(
                f"cd ../Convertors/mace-master &&python3 tools/python/run_model.py --config ../../opTest/mace/{model_name} --benchmark --runtime=cpu --vlog_level=2",
                shell=True)
            # frequency_monitor.kill()
            with open("adbLogs/mace/" + model_name + '_cpu.log', 'wb+') as f:
                f.write(log)
        except subprocess.CalledProcessError as e:
            with open("adbLogs/mace/err/" + model_name + '_cpu.log', 'wb+') as f:
                f.write(e.output)
            print(e.output)
            print(e.stdout)
            print(e.stderr)
    # for model_name in os.listdir("./Convertors/MACE_models/GPU"):
    #     if not model_name.endswith(".yaml"):
    #         continue
    #     try:
    #         frequency_monitor = subprocess.Popen(
    #             f'adb shell "top -d 0.01" |grep mace_run  >./adbLogs/cpuLogs/mace/{model_name}.gpu.log',
    #             shell=True)
    #         log = subprocess.check_output(
    #             f"cd Convertors/mace-master &&python3 tools/python/run_model.py --config ../MACE_models/GPU/{model_name} --benchmark --runtime=gpu --vlog_level=2",
    #             shell=True)
    #         frequency_monitor.kill()
    #
    #         with open("adbLogs/mace/" + model_name + '_gpu.log', 'wb+') as f:
    #             f.write(log)
    #     except subprocess.CalledProcessError as e:
    #         print(e.output)
    #         with open("adbLogs/mace/err/" + model_name + '_gpu.log', 'wb+') as f:
    #             f.write(e.output)
    #         print(e.stdout)
    #         print(e.stderr)


def analyse():
    for filename in os.listdir("adbLogs/mace"):
        if '.log' not in filename:
            continue

        flag = 0
        content = ""
        first=0.0
        op=[]
        times=[]
        index=0
        for line in open("adbLogs/mace/" + filename,encoding='unicode_escape').readlines():
            if line.startswith(
                    "I /home/runner/work/DLFrameworkProj/DLFrameworkProj/Convertors/mace-master/mace/utils/statistics.cc:343]"):
                if '|' in line:
                    if flag == 0 and 'Op Type' not in line:
                        flag = 1
                    typs = re.findall(r"^\s*\|\s*(\S+?)\s*\|\s*(\S+?)\s*\|.+?\|", line.replace("I /home/runner/work/DLFrameworkProj/DLFrameworkProj/Convertors/mace-master/mace/utils/statistics.cc:343]",""))

                    if len(typs) > 0:
                        print(typs)
                        print(float(typs[0][1]))

                        time = round(float(typs[0][1]) - first, 3)
                        print(time)
                        first = float(typs[0][1])
                        op.append(typs[0][0])
                        # times.append(time)
                        if index > 0:
                            times.append(time)
                        index += 1

                        # print(f'{typs[0][0]}\t{time}',file=res_cpu)

                else:
                    # print(line)
                    # print(flag)
                    # print(index)

                    if flag == 1:
                        times.append(0.0)
                        for i in range(0, index):
                            content += f'{op[i]}\t{times[i]}\n'

                        with open(f"csv/mace/{filename}.log","w+") as f:
                            print(content, file=f)
                        break



if __name__ == '__main__':
    # prepare()
    run()
    analyse()
