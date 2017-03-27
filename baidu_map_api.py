#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 项目简述: 利用百度地图api,把经纬度转成街道信息
# 项目名称: gps_data_processing 
# 文件名: baidu_map_api 
# 创建日期: 2016/10/15 
# __author__ = "yangmu"
from usbinfo import usbinfo
import ConfigParser
import requests
import yaml
import os
import sys
import logging


def gen_bd_address(latitude, longitude):
    """
    通过gps模块的经纬度来获取对应的街道地址
    :param lat:
    :param lng:
    :return:
    """
    cf = ConfigParser.ConfigParser()
    cf.read("gps.conf")
    ret_addr = cf.get("default_addr", "addr")
    url = 'http://api.map.baidu.com/geocoder/v2/?' + \
          'ak={bd_map_ak}&location={lat},{lng}'.format(lat=latitude, lng=longitude,
                                                       bd_map_ak=cf.get("map_key", "key")) + \
          '&callback=&output=json&pois=0&coordtype=wgs84ll'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
    try:
        r = requests.get(url, headers=headers)
        r_json = r.json()
    except Exception as e:
        ##        msg = u'出现异常: 未能获取到对应的街道信息!'
        ##        logging.warning(msg)
        ##        print(msg)
        return ret_addr

    return r_json['result']['formatted_address']


if __name__ == "__main__":
    ##    latitude = 39.898167
    ##    longitude = 116.662940
    latitude = 40.064818
    longitude = 116.542737
    dt_address = gen_bd_address(latitude, longitude)
    print(dt_address)
