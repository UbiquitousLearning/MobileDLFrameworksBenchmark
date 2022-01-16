#  @Time    : 2021/8/28 下午9:58
#  @Author  : lixiang
#  @FileName: convertor.py
#
import os
import subprocess

from MACE import MACE
from MNN import MNN

for filename in os.listdir("tf_models"):
    if filename.endswith(".pb"):

        print(filename)


    # try:
    #
    #     # MNN(os.path.abspath(f"./tf_models/{filename}"))
    # except Exception as e:
    #     print(e)
        try:

            MACE(os.path.abspath(f"./tf_models/{filename}"))
        except Exception as e:
            print(e)