#!/usr/bin/python
# -*-coding:utf-8-*-
# 项目简述: 把默认格式的经纬度信息，转换成为百度地图api能够识别的经纬度格式
# 项目名称: gps_data_processing
# 文件名: conv_usbinfo 
# 创建日期: 2016/10/15 
# __author__ = "yangmu"
# /*20170318 zhoulei*/ 增加判断usbinfo返回值是否是否为空

import ConfigParser
from usbinfo import usbinfo
from baidu_map_api import gen_bd_address


def lon_lat_Conv(a):
    a = usbinfo()
    if a:
        num1 = a[1]
        num2 = a[0]
        if num1 == num2 == '':
            cf = ConfigParser.ConfigParser()
            cf.read("gps.conf")
            lon = cf.get("default_lon_lat", "lon")
            lat = cf.get("default_lon_lat", "lat")
            mylist = list()
            mylist.append(lat)
            mylist.append(lon)
            return mylist
        a1 = (float(num1) / 100)
        a1_str = str(a1)
        a1_str3 = a1_str[:3]

        b1 = a1_str[4:]
        if len(b1) == 6:
            b1 = b1 + str(0)
        if len(b1) == 5:
            b1 = b1 + str(0) + str(0)

        b1_f = float(b1)
        b1_1 = b1_f / 60
        bb1 = round(b1_1, 1)

        c1_str = str(bb1 * 10)
        aaa1 = float(a1_str3 + c1_str)

        a2 = (float(num2) / 100)
        a2_str = str(a2)
        a2_str3 = a2_str[:2]

        b2 = a2_str[3:]
        if len(b2) == 6:
            b2 = b2 + str(0)
        if len(b2) == 5:
            b2 = b2 + str(0) + str(0)

        b2_f = float(b2)
        b2_1 = b2_f / 60
        bb2 = round(b2_1, 1)

        c2_str = str(bb2 * 10)
        aaa2 = float(a2_str3 + c2_str)

    mylist = list()
    if int(num1[3]) == 0 and int(num1[4]) != 0 and int(num2[2]) == 0 and int(num2[3]) != 0:
        print '经纬度转换后小数点第一位均为0'
        x = float(str(aaa1 / 10000)[:3] + str(0) + str(bb1 * 10))
        y = float(str(aaa2 / 10000)[:2] + str(0) + str(bb2 * 10))
        mylist.append(y / 1000000)
        mylist.append(x / 1000000)
        return mylist
    if int(num1[3]) == 0 and int(num1[4]) != 0:
        print '经度转换后小数点第一位为0'
        if len(str(aaa1)) == 10:
            x = float(str(aaa1 / 10000)[:3] + str(0) + str(bb1 * 10))
            mylist.append(aaa2 / 1000000)
            mylist.append(x / 1000000)
            return mylist
        x = float(str(aaa1 / 10000)[:3] + str(bb1 * 10))
        mylist.append(aaa2 / 1000000)
        mylist.append(x / 1000000)
        return mylist

    if int(num1[3]) == 0 and int(num1[4]) == 0:
        print '经度转换后小数点后两位均为0'
        if len(str(aaa1)) == 9:
            x = float(str(aaa1 / 10000)[:3] + str(0) + str(0) + str(bb1 * 10))
            mylist.append(aaa2 / 1000000)
            mylist.append(x / 1000000)
            return mylist
        x = float(str(aaa1 / 10000)[:3] + str(0) + str(0) + str(bb1 * 10))
        mylist.append(aaa2 / 1000000)
        mylist.append(x / 10000000)
        return mylist
    if int(num2[2]) == 0 and int(num2[3]) != 0:
        print '纬度转换后小数点第一位为0'
        if len(str(aaa2)) == 10:
            x = float(str(aaa2 / 10000)[:2] + str(bb2 * 10))
            mylist.append(x / 1000000)
            mylist.append(aaa1 / 1000000)
            return mylist
        x = float(str(aaa2 / 10000)[:2] + str(0) + str(bb2 * 10))
        mylist.append(x / 1000000)
        mylist.append(aaa1 / 1000000)
        return mylist
    if int(num2[2]) == 0 and int(num2[3]) == 0:
        print '纬度转换后小数点后两位均为0'
        if len(str(aaa2)) == 8:
            x = float(str(aaa2 / 10000)[:2] + str(0) + str(0) + str(bb2 * 10))
            print x
            mylist.append(x / 1000000)
            mylist.append(aaa1 / 1000000)
            return mylist
        x = float(str(aaa2 / 10000)[:2] + str(0) + str(bb2 * 10))
        mylist.append(x / 1000000)
        mylist.append(aaa1 / 1000000)
        return mylist
    mylist.append(aaa2 / 1000000)
    mylist.append(aaa1 / 1000000)
    return mylist


if __name__ == '__main__':
    print lon_lat_Conv(['4000.68908', '11641.16320'])
