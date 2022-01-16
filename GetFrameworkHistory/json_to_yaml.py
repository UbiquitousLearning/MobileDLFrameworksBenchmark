#  @Time    : 2021/8/1
#  @Author  : lixiang
#  @FileName: json_to_yaml.py


import copy
import json
import yaml
lists=json.load(fp=open("ncnn_commits.json"))
template=yaml.load(open("tf_compile_template.yaml"))
template_job=template['jobs']['android-aarch64-gpu']
template['jobs']=[]


def list_of_groups(init_list, childern_list_len):
    '''
    init_list为初始化的列表，childern_list_len初始化列表中的几个数据组成一个小列表
    :param init_list:
    :param childern_list_len:
    :return:
    '''
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list
sub_lists=list_of_groups(lists,20)
sub_list_group=list_of_groups(sub_lists,5)
def trim_time(time:dict)->dict:
    time['time']=time['time'].split("T")[0]
    print(time)
    return time
print(len(sub_list_group))
for i in range(0, len(sub_list_group)):
    jobs_list={}
    for j in range(0,len(sub_list_group[i])):
        template_job['strategy']={"matrix":{"include":list(map(trim_time,sub_list_group[i][j]))},"fail-fast":False}
        jobs_list[f'android-aarch64-gpu{i+j}']=copy.deepcopy(template_job)
    template['jobs']=jobs_list
    with open(f"tflite_{i}.yaml","w+") as f:
        print(yaml.dump(template),file=f)
