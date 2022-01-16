#!/bin/bash

#
#  @Time    : 2021/8/30 上午9:56
#  @Author  : lixiang
#  @FileName: MNN.sh
#
#

ls ./tf_models
LD_LIBRARY_PATH=.
find ./tf_models -name '*.pb'  | while read i
do
        echo "$i";
        ./MNNConvert -f TF --modelFile "$i" --MNNModel "${i/.pb/.mnn}" --bizCode biz

done

find ./tf_models -name '*.mnn'  | while read i
do
        echo "$i";
        mv "$i" ./MNN_models
done