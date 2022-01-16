#  @Time    : 2021/10/12 下午9:29
#  @Author  : lixiang
#  @FileName: main.py
#
import os
import re
import subprocess

from adbutils import AdbTimeout

import mace
# import MNN
import snpe
import tflite
import ncnn
import adbutils

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
# try:
#     adb.connect("112.13.171.113:9999", timeout=3.0)
# except AdbTimeout as e:
#     print(e)
print(adb.device_list())
for d in adb.devices():
    print(d.serial)
d = adb.device()

mace.prepare()
mace.run()
mace.analyse()

ncnn.prepare(d)
ncnn.run(d)
ncnn.analyse()

tflite.prepare(d)
tflite.run(d)
tflite.analyse()

snpe.prepare(d)
snpe.run(d)
snpe.analyse()
