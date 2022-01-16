#  @Time    : 2022/1/16 下午10:16
#  @Author  : lixiang
#  @FileName: download_artifacts.py



import os
from concurrent.futures import ThreadPoolExecutor, wait,ALL_COMPLETED

import requests
import zipfile
OWNER="lx200916"
REPO="ncnn"
token=""
headers = {
  'Authorization': f'Bearer {token}' # Replace with Ur Token.
}
r=requests.session()
r.headers=headers
# run_id=[{'name':'v8_1','id':1087399118},{'name':'v8_2','id':1087399122},{'name':'v8_2v','id':1087399124},{'name':'v8_3','id':1087399123}]
run_id=[{'name':'n_1','id':1371191156},{'name':'n_1v','id':1371191899},]
executor = ThreadPoolExecutor(max_workers=5)

def getartifact(artifact:dict,pwd:str):
    file=r.get(artifact['archive_download_url']).content
    # print(file)
    path=pwd+"/"+artifact['name']
    print(path)
    with open(path+'.zip',"wb+") as f:
        f.write(file)
    zipfile.ZipFile(path+'.zip').extractall(path=path)


for item in run_id:
    all_task=[]

    if not os.path.exists(f"{REPO}/{item['name']}"):
        os.makedirs(f"{REPO}/{item['name']}")
    aList=r.get(f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{item['id']}/artifacts?per_page=100&page=1").json()
    if aList['total_count']>100:
        print("More Than One Page")
    print(aList['total_count'])
    for artifact in aList['artifacts']:
        all_task.append(executor.submit(getartifact,artifact=artifact,pwd=f"{REPO}/{item['name']}"))
    wait(all_task,return_when=ALL_COMPLETED)






