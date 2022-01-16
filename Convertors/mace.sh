#
#  @Time    : 2021/8/30 下午6:53
#  @Author  : lixiang
#  @FileName: mace.sh
#
#

cp ./mace_models/*.yaml ./
cd mace-master
ls |grep .ymal
find ../ -name '*.yaml' -maxdepth 1  | while read i
do
        echo "$i";
        python3 tools/python/convert.py --config "$i"

done