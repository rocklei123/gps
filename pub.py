#!/usr/bin/python
# -*-coding:utf-8-*-
import redis
from get_addr import get_addr
from usbinfo import usbinfo
from conv_usbinfo import lon_lat_Conv
import datetime
import time
import ConfigParser
import MySQLdb
from baidu_map_api import gen_bd_address

cf = ConfigParser.ConfigParser()
cf.read("gps.conf")
frequency = float(cf.get("frequency", "myfrequency"))
channel = cf.get("channel", "mychannel")

default_lat = cf.get("default_lon_lat", "lat")

gis_mode = cf.get("GIS_MODE", "gis_mode")
gis_frequency = int(cf.get("GIS_FREQUENCY", "gis_frequency"))

car_id = cf.get("CAR_ID", "car_id")
car = car_id.decode('gbk').encode('utf-8')

host = cf.get("MYSQL_INFO", "host")
port = int(cf.get("MYSQL_INFO", "port"))
user = cf.get("MYSQL_INFO", "user")
passwd = cf.get("MYSQL_INFO", "passwd")
db = cf.get("MYSQL_INFO", "db")

rc = redis.Redis(host='127.0.0.1')
##ps = rc.pubsub()

for num in range(1, 360000):
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mylist = lon_lat_Conv(usbinfo)
    ##    mystr=str(mylist[1])+','+str(mylist[0])+','+str(cur_time)
    mydict = {"latitude": float(mylist[0]), "current_time": str(cur_time), "longitude": float(mylist[1])}
    ##    print("Publish To Redis gps_data_ch :"+mydict)

    ##    mydict={"current_time":cur_time,"current_address":cur_addr}
    print "Publish To Redis channel :" + str(mydict.get('latitude')) + ',' + str(
        mydict.get('longitude')) + ',' + mydict.get('current_time')

    ##    print gen_bd_address(mylist[0],mylist[1])
    ##    print mydict
    ##    print type(mydict)

    ##    if num%gis_frequency==0 and gis_mode=='on':
    if num % gis_frequency == 0 and gis_mode == 'on' and str(mylist[0]) != default_lat:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )
        cur = conn.cursor()
        print 'insert into mysql!!!!!!!!!!!!!!!!!!!!!!!!!!'
        sqli = "insert into base_info(car_id,lon,lat,time) values(%s,%s,%s,%s)"
        cur.execute(sqli, (car, str(mydict.get('longitude')), str(mydict.get('latitude')), cur_time))
        cur.close()
        conn.commit()
        conn.close()

    rc.publish(channel, mydict)
    time.sleep(frequency)
