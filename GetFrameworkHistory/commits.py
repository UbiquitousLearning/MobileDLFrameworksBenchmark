#  @Time    : 2021/7/31
#  @Author  : lixiang
#  @FileName: main.py

import json
import time

import requests
import datetime
OWNER="tencent"
REPO="ncnn"
FileName='ncnn'
# AccessToken Expires on Sun, Aug 29 2021.
token=""
headers = {
  'Authorization': f'Bearer {token}' # Replace with Ur Token.
}

def get_sunday_dates(startTime: datetime.datetime) -> list[str]:
    day_list = []
    start_sunday = startTime + datetime.timedelta(days=6 - startTime.weekday())
    now = datetime.datetime.now()
    # now=datetime.datetime.strptime( "2020-08-11","%Y-%m-%d")
    while start_sunday < now:
        start_sunday=start_sunday + datetime.timedelta(days=7)
        day_list.append(datetime.datetime.strftime(start_sunday, "%Y-%m-%d"))
    return day_list


start_date = datetime.datetime.strptime( "2018-02-16","%Y-%m-%d")
date_list=get_sunday_dates(start_date)
print(date_list)


commit_list=[]

for item in range(0,len(date_list)):
    print(date_list[item])
    since_str=f"since={date_list[item-1]}T23:59:59-7000&"
    if(item==0):
        since_str=""
    commits=requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/commits?{since_str}until={date_list[item]}T23:59:59-7000&per_page=1&page=1",headers=headers).json()
    print(commits)
    if(len(commits))==0:
        continue
    print(commits[0]['sha'])
    commit=commits[0]
    commit_list.append({"sha":commit['sha'],"time":commit['commit']['committer']['date']})
    time.sleep(0.5)

print(date_list)
with open(f"{FileName}_commits.json","w+") as f:
    print(json.dumps(commit_list),file=f)
