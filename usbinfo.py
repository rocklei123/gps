#!/usr/bin/python
# -*-coding:utf-8-*-
# 项目简述: 利用python串口模块serial读取gps设备传输进来的信息，并获取默认格式的经纬度
# 项目名称: gps_data_processing 
# 文件名: usbinfo 
# 创建日期: 2016/10/15 
# __author__ = "yangmu"
#
# /*20170319 zhoulei
# 1 增加设备判断
# 2 增加从linux 设备接受gps数据并处理
# 3 修复一次性获取一行数据导致无$GPRMC关键字时定位默认地址的问题
# 4 增加一次性获整个NMEA协议格式的完整数据包
# */
#


import serial
import ConfigParser
import time
import platform


def usbinfo():
    cf = ConfigParser.ConfigParser()
    cf.read("gps.conf")
    # get linux paramter
    myLinuxDev = cf.get("linuxDev", "myLinuxDev")
    myLinuxPort = cf.get("linuxPort", "myLinuxPort")

    # get windows paramter
    myWinDev = cf.get("winDev", "myWinDev")
    myWinPort = cf.get("winPort", "myWinPort")

    myTimeOut = cf.get("timeOut", "myTimeOut")
    sysstr = platform.system()
    try:
        if (myWinDev != "" or myLinuxDev != ""):
            if (sysstr == "Windows"):
                ser = serial.Serial(port=myWinDev, baudrate=myWinPort, timeout=2)
                print 'Running......'
            elif (sysstr == "Linux"):
                ser = serial.Serial(port=myLinuxDev, baudrate=myLinuxPort, timeout=2)
                print 'Running......'
            else:
                return
    except Exception, e:
        print 'failed!!!'
        print e
        ser.close()
        time.sleep(1)
        usbinfo()

    time.sleep(1)
    print 'ok'

    try:
        while True:
            s = ser.readline()
            if s.startswith('$GPRMC,'):
                string_gps = s.split(',')
                a = list()
                a.append(string_gps[3])
                a.append(string_gps[5])
                ser.close()
                return a

    except Exception, e:
        print '222222222222'
        print e
        ser.close()
        time.sleep(1)
        usbinfo()


if __name__ == '__main__':
    ##    usbinfo()
    cf = ConfigParser.ConfigParser()
    cf.read("gps.conf")
    mydev = cf.get("dev", "mydev")
    print mydev
