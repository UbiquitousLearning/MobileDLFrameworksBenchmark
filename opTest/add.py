#  @Time    : 2021/10/9 下午7:09
#  @Author  : lixiang
#  @FileName: add.py
#

# @Time    : 2021/10/9 7:09 下午
# @Author  : lixiang
# @FileName: add.py
import re

mace_csv=open('./adbLogs/mace/csv/vgg16.log.info.csv')
ncnn_csv=open('./adbLogs/ncnn/csv/vgg16.log')
tflite_csv=open('./adbLogs/tflite/csv/vgg16.log.info.csv')
time_sum=0.0
file_list=[mace_csv,ncnn_csv,tflite_csv]
reg=re.compile(r'^//\S+\s+(\d+.\d*)')
i=0
for fileName in file_list:
    for line in fileName.readlines():
        if line.startswith('//'):
            strL=reg.findall(line)
            if len(strL)>0:
                print(strL)
                print(float(strL[0]))
                time_sum+=round(float(strL[0]),2)
                i+=1
print(time_sum)
print(i)
