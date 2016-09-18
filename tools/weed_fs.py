#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weed_fs.py
@time: 16-9-18 上午10:41
"""


from config import WEED_FS
import requests


def _get_assign():
    """
    获取分配的资源（url fid）
    {"fid":"1,014e123ade","url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080","count":1}
    """
    url = '%s/dir/assign' % WEED_FS
    return requests.get(url).json()


def _get_locations(fid):
    """
    获取文件服务器列表
    {"volumeId":"1","locations":[{"url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080"}]}
    """
    volume_id = fid.split(',')[0]
    url = '%s/dir/lookup?volumeId=%s' % (WEED_FS, volume_id)
    return requests.get(url).json()


def save_file(file_path):
    """
    保存文件
    {"name":"test.csv","size":425429}
    """
    assign = _get_assign()
    url = '%s/%s' % (assign['url'], assign['fid'])
    res = requests.post(url, files={'file': open(file_path, 'rb')})
    return res.json()


def get_file_path(fid, separator=None):
    """
    获取文件路径
    """
    locations = _get_locations(fid)
    public_url = locations['locations'][0]['publicUrl']
    return 'http://%s/%s' % (public_url, fid.replace(',', separator) if separator else fid)


if __name__ == '__main__':
    print get_file_path('1,014e123ade')
    print get_file_path('1,014e123ade', '/')
