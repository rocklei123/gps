# Recieve GPS Data and process
从串口获取GPS设备收集的经纬度、速度数据，并将经纬度数据转换为百度地图可识别的点分十进制经纬度，同时将经纬度转换成地址信息，然后组合成json字符串发送至服务端处理。

1、GPS设备为u-blox
2、Python程序从串口获取（可同时获取linux主机串口、windows主机串口数据）
