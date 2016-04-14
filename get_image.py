#!/usr/bin/python
#encoding:utf-8
'''
因为docker pull 日了狗的分层机制，以至于在a服务器上通过代理拉到镜像后，在b服务器上仍然可能需要再拉取一些新的层，因为那些层在a服务器上本来就有！
所有不得不自己写一个pull 方法，保证拉到所有的层缓存到代理服务器
'''
import requests
import json
import sys
import os
import urllib3
DOCKERHUB = 'dockerhub.my.com'
requests.packages.urllib3.disable_warnings()
def get_blobs(image_name,tag):
    manitests_url  = "https://"+DOCKERHUB+'/v2/'+image_name+'/manifests/'+tag
    r = requests.get(manitests_url,verify=False)
    blob_list = eval(r.text)["fsLayers"]
    blobs = []
    for line in blob_list:
        blobs.append(line.values()[0])
    return blobs

def get_all_file(image_name,tag):
    file_start_url = "https://"+DOCKERHUB+'/v2/'+image_name+'/blobs/'
    blobs = get_blobs(image_name,tag)
    for blob in blobs:
        f = open(os.devnull, 'wb')
        url = file_start_url+blob
        r = requests.get(url,verify=False)
        f.write(r.content)
        if r.status_code != 200:
            raise IndexError,"get failed "+url

if __name__ == "__main__":
    image_name = sys.argv[1]
    tag = sys.argv[2]
    get_all_file(image_name,tag)

