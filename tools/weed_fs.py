#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weed_fs.py
@time: 16-9-18 上午10:41
"""

from config import REQUESTS_TIME_OUT
from config import WEED_FS
import requests
import csv


def _get_assign():
    """
    获取分配的资源（url fid）
    正确:
        {"fid":"1,014e123ade","url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080","count":1}
    错误:
        {"error":"No free volumes left!"}
    """
    url = '%s/dir/assign' % WEED_FS
    res = requests.get(url, timeout=REQUESTS_TIME_OUT).json()
    if 'error' in res:
        raise Exception(res['error'])
    return res


def _get_locations(fid):
    """
    获取文件服务器列表
    {"volumeId":"1","locations":[{"url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080"}]}
    """
    volume_id = fid.split(',')[0]
    url = '%s/dir/lookup?volumeId=%s' % (WEED_FS, volume_id)
    return requests.get(url, timeout=REQUESTS_TIME_OUT).json()


def save_file(file_path):
    """
    保存本地文件至weed_fs文件系统
    {"name":"test.csv","size":425429}
    """
    assign = _get_assign()
    url = 'http://%s/%s' % (assign['url'], assign['fid'])
    res = requests.post(url, files={'file': open(file_path, 'rb')}, timeout=REQUESTS_TIME_OUT)
    return dict(res.json(), **assign)


def get_file_url(fid, separator=None):
    """
    获取文件链接
    """
    locations = _get_locations(fid)
    public_url = locations['locations'][0]['publicUrl']
    return 'http://%s/%s' % (public_url, fid.replace(',', separator) if separator else fid)


def read_csv(fid, encoding=None):
    """
    逐行读取远程csv文件
    :param fid:
    :param encoding: 'gbk'/'utf-8'
    :return:
    """
    file_url = get_file_url(fid)
    download = requests.get(file_url, timeout=REQUESTS_TIME_OUT)
    csv_rows = csv.reader(download.iter_lines(), delimiter=',', quotechar='"')
    for csv_row in csv_rows:
        line = [item.decode(encoding, 'ignore') if encoding else item for item in csv_row]
        yield line


if __name__ == '__main__':
    # 获取文件链接
    print get_file_url('1,014e123ade')
    print get_file_url('1,014e123ade', '/')
    # 读取远程csv文件
    rows = read_csv('1,014e123ade', 'gbk')
    for row in rows:
        print row
