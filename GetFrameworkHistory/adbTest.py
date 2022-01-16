import subprocess
import os

REPO = "ncnn"
import adbutils


logf = open("run.log", "w+")
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
print(adb.device_list())
for d in adb.devices():
    print(d.serial)
d = adb.device()

for parent, dirnames, filenames in os.walk(REPO, followlinks=True):
    # For NCNN
    if 'benchncnn' in filenames:
        print(parent,file=logf)
        file_path = os.path.join(parent, 'benchncnn')
        params_file_path = os.path.join(parent, '*.param')

        path_info = parent.split("/")

        if 'v'  in path_info[1]:
            vu_flag="v"
        else:
            vu_flag="n"
        if 'int8' in path_info[1]:
            int8_flag = "int8"
        else:
            int8_flag = "n"

        log_filename=f"adbLogs/{path_info[0]}/{path_info[0]}_{vu_flag}_{int8_flag}_{path_info[2]}.log"
        print(subprocess.run(["adb" ,"push",f"{os.getcwd()}/{file_path}", "/data/local/tmp/" ],stderr=subprocess.STDOUT))
        print(subprocess.run(f"adb push {os.getcwd()}/{params_file_path} /data/local/tmp/",shell=True,stderr=subprocess.STDOUT))

        log=d.shell("cd /data/local/tmp/ &&chmod 777 benchncnn &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchncnn 4 8 0 1 1")
        print(log)
        with open(log_filename,'w+') as f:
            f.write(log)
        # exit(1)
        print(log_filename,file=logf)
    # For TfLite
    # if 'benchmark_model' in filenames:
    #     print(parent, file=logf)
    #     file_path = os.path.join(parent, 'benchmark_model')  # TODO:根据不同框架修改
    #     # params_file_path = os.path.join(parent, '*.param')
    #
    #     path_info = parent.split("/")
    #
    #     log_filename = f"adbLogs/{path_info[0]}/{path_info[0]}_{path_info[2]}.log"
    #     print(
    #         subprocess.run(["adb", "push", f"{os.getcwd()}/{file_path}", "/data/local/tmp/"], stderr=subprocess.STDOUT))
    #     # print(subprocess.run(f"adb push {os.getcwd()}/{params_file_path} /data/local/tmp/",shell=True,stderr=subprocess.STDOUT))
    #     # TODO:根据不同框架修改
    #     frequency_monitor = subprocess.Popen('adb shell "cd /data/local/tmp/ &&./frequency_monitor.sh freq_temperature.result 0.002"',
    #                                          shell=True)
    #     log = d.shell(
    #         "cd /data/local/tmp/ &&chmod +x benchmark_model &&export LD_LIBRARY_PATH=/data/local/tmp &&./benchmark_model --graph=mobilenet_quant_v1_224.tflite --num_threads=8")
    #     frequency_monitor.kill()
    #     d.sync.pull("/data/local/tmp/freq_temperature.result", log_filename.replace(".log", ".result"))
    #     d.shell('rm /data/local/tmp/freq_temperature.result')
    #     with open(log_filename, 'w+') as f:
    #         f.write(log)
    #     # exit(1)
    #     print(log_filename, file=logf)
    #     # exit(0)
