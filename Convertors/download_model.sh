#
#  @Time    : 2021/8/30 下午1:49
#  @Author  : lixiang
#  @FileName: download_model.sh
#
#
cd tf_models
find ./ -name '*.sh'  | while read i
do
        bash $i >/dev/null 2>&1

done
ls