#!/usr/bin/python
# -*-coding:utf-8-*-
# 项目简述: 利用python串口模块serial读取gps设备传输进来的信息，并获取默认格式的经纬度
# 项目名称: gps_data_processing 
# 文件名: usbinfo 
# 创建日期: 2016/10/15 
# __author__ = "zhoulei"
#
# /*20170319 zhoulei
# 1 增加设备判断
# 2 增加从linux 设备接受gps数据并处理
# 3 修复一次性获取一行数据导致无$GPRMC关键字时定位默认地址的问题
# 4 增加一次性获整个NMEA协议格式的完整数据包
# 5 获取PC下串口的名称(否则usb设备拔掉在插入串口会改变)
# */
#


import serial
import ConfigParser
import time
import platform
import string
import traceback
import serial.tools.list_ports
from decimal import Decimal

def usbinfo():
    # 以下行数据测试完成后需要删除,仅在测试时使用
    #s = '$GPRMC,024813.640,A,3158.4608,N,11848.3737,E,10.05,324.27,150706,,,A*50'
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
    gpsDataList = list()
    ser = None
    a = list()
    try:
        if (sysstr == "Windows"):
            plist = list(serial.tools.list_ports.comports())
            if len(plist) <= 0:
                print "The Serial port can't find!"
            else:
                plist_0 = list(plist[0])
                serialName = plist_0[0]
                ser = serial.Serial(port=serialName, baudrate=myWinPort, timeout=2)
                print "Running : u-blox 6 GPS Receiver on windows  now is using port ", ser.name
        elif (sysstr == "Linux"):
            if (myLinuxDev != ""):
                ser = serial.Serial(port=myLinuxDev, baudrate=myLinuxPort, timeout=2)
                print 'Running: u-blox 6 GPS Receiver on Linux '
        else:
            return

        if ser.isOpen():
            s = ser.read(1024)
            if s != "" and s is not None:
                #print "s===" , s
                tem = s.split('\n')
                for line in tem:
                    if line.startswith('$GPRMC,'):
                        print "usbinfo.py  GPRMC data=====:" + line
                        string_gps = line.split(',')
                        a.append(string_gps[3])
                        a.append(string_gps[5])
                        strknot = string_gps[7]
                        if strknot is not None and strknot != "":
                            knot = (string.atof(strknot)) * 1.852
                            speed = Decimal(knot).quantize(Decimal('0.00'))
                            a.append(speed)
                        ser.close()
                        return a
    except Exception, e:
        print 'Exception*** usbinfo.py : get GPS data from COM failed!!!'
        print e
        return

if __name__ == '__main__':
    ##    usbinfo()
    cf = ConfigParser.ConfigParser()
    cf.read("gps.conf")
    mydev = cf.get("dev", "mydev")
    print mydev
