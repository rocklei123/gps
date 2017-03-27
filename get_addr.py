#!/usr/bin/python
# -*-coding:utf-8-*-
# 项目简述: 把gps设备读取并处理之后的经纬度转换成为真实街道地址
# 项目名称: gps_data_processing
# 文件名: get_addr
# 创建日期: 2016/10/15 
# __author__ = "yangmu"
# /*20170319 zhoulei*/ 增加判断mylist 是否为空

from conv_usbinfo import lon_lat_Conv
from usbinfo import usbinfo
from baidu_map_api import gen_bd_address


def get_addr():
    mylist = lon_lat_Conv(usbinfo)
    # print '经过转换过后的经纬度为：'
    # print str(mylist)
    if mylist:
        return gen_bd_address(mylist[0], mylist[1])


if __name__ == "__main__":
    print get_addr()
