#!/usr/bin/python
#author zhoulei
#
#程序主入口(可将数据传入redis通道、可传入Java端做处理等)
#
#-*-coding:utf-8-*-
import redis
from usbinfo import usbinfo
from conv_usbinfo import lon_lat_Conv
import datetime
import time
import ConfigParser
from getGpsJsonStr import  getGpsOfJsonStr
from gpsClient import *

cf = ConfigParser.ConfigParser()
cf.read("gps.conf")
frequency=float(cf.get("frequency", "myfrequency"))
channel=cf.get("channel", "mychannel")
default_lat=cf.get("default_lon_lat","lat")
gis_mode=cf.get("GIS_MODE","gis_mode")
gis_frequency=int(cf.get("GIS_FREQUENCY","gis_frequency"))

car_id=cf.get("CAR_ID","car_id")
car=car_id.decode('gbk').encode('utf-8')

rc = redis.Redis(host='127.0.0.1')
##ps = rc.pubsub()

for num in range(1,360000):
    print '-------------------------------------------------------------------' , num
    gislist =lon_lat_Conv()
    if gislist is not None :
        mylist = list()
        mylist.append(gislist[0])
        mylist.append(gislist[1])
        print "redis  list ===",mylist
        print "gis list===",gislist
        cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        mydict={"latitude":float(mylist[0]),"current_time":str(cur_time),"longitude":float(mylist[1])}
        print "Publish To Redis channel :"+str(mydict.get('latitude'))+','+str(mydict.get('longitude'))+','+mydict.get('current_time')
        if num%gis_frequency==0 and gis_mode=='on' and str(gislist[0])!=default_lat:
            print 'Publish To Netty Server**************************'
            msg = getGpsOfJsonStr(gislist,car_id)
            if msg is not None:
                try :
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client = doConnect(s)
                    revice = sendData(client, msg)
                    doClose(client)
                except Exception, e:
                    print e

        rc.publish(channel, mydict)
    time.sleep(frequency)
