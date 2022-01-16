#  @Time    : 2021/8/27 下午1:09
#  @Author  : lixiang
#  @FileName: MNN.py
#

#  @Time    : 2021/8/27 下午1:08
#  @Author  : lixiang
#  @FileName: MNN.py
#
import os
import subprocess
import shutil


def MNN(filepath):
    filename=filepath.split("/")[-1]
    output_name = filename.replace('.pb', '.mnn')
    print(os.getcwd())
    out = subprocess.check_output(f"export LD_LIBRARY_PATH=. &&./MNNConvert -f TF --modelFile {filename} --MNNModel {output_name} --bizCode biz",
                                  shell=True)
    print(out)
    shutil.copy(filepath.replace(".pb", '.mnn'), f"./MNN_models/{output_name}")



