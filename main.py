#  @Time    : 2021/9/8 下午9:17
#  @Author  : lixiang
#  @FileName: test.py
#

#  @Time    : 2021/9/8 下午8:27
#  @Author  : lixiang
#  @FileName: test.py
#
import os

import adbutils
from adbutils import AdbTimeout

import mace
import MNN
import ncnn
import pytorchm
import tflite
import snpe

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
# We also support Remote ADB Connection.
# try:
#     adb.connect("xxxx.xxx.xxx.xxx:9999", timeout=3.0)
# except AdbTimeout as e:
#     print(e)
print(adb.device_list())
for d in adb.devices():
    print(d.serial)
d = adb.device()

#mace
# mace.prepare()
# mace.run()
# mace.analyse()
#
# #MNN
MNN.prepare(d)
MNN.run(d)
MNN.analyse()
#
# # #NCNN
ncnn.prepare(d)
ncnn.run(d)
ncnn.analyse()
# #
# # #tflite
tflite.prepare(d)
tflite.run(d)
tflite.analyse()
# #
# # #snpe
snpe.prepare(d)
snpe.run(d)
# snpe.analyse()
#
# #pytorch
pytorchm.prepare(d)
pytorchm.run(d)
pytorchm.analyse()

os.system("echo \007")