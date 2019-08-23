# -*- coding: utf-8 -*-
# 本文件存放拓展方法
"""
analysis_data未解析方法，设计为传入报文，
根据协议拆分为消息头，消息体
然后根据协议的组装，解析消息头
根据解析的消息头，解析消息体
当前只有0x0200=512的消息体解析，而且没有解析附加消息和传感器消息
"""
import sys
import re
from jctool import jctool
jctool = jctool()
reload(sys)
sys.setdefaultencoding('utf8')
class analysis_data(object):
    def __init__(self):
        pass
    def data_ano(self,msg):
        #接收报文转义
        data=jctool.dd(msg)
        #拆分消息头和消息体
        datahead=data[2:26]
        databody=data[26:-2]
        msgHead=self.head_ano(datahead)
        if msgHead.get("msgID")==512:
            msgBody=self.body_ano_512(databody)
        else:
            msgBody=""
        print {"msgHead":msgHead,"msgBody":msgBody}
        return {"msgHead":msgHead,"msgBody":msgBody}
    def head_ano(self,head):
        datahead=head.replace(" ","")
        msgID=jctool.to_int(datahead[0:4])#消息id
        bodySize=jctool.to_int(datahead[4:8])#消息体属性
        msgSN=jctool.to_int(datahead[20:24])#流水号
        mobile=str(int(datahead[8:20].replace(" ","")))#手机号
        msgHead={"msgSN":msgSN,"msgID":msgID,"bodySize":bodySize,"mobile":mobile}
        return msgHead
    def body_ano_512(self,body):
        databody=body.replace(" ","")
        alarm=jctool.to_int(databody[0:8])#报警
        status=jctool.to_int(databody[8:16])#状态
        originalLatitude=float(jctool.to_int(databody[16:24]))/1000000 #纬度
        originalLongitude=float(jctool.to_int(databody[24:32]))/1000000 #经度
        altitude=jctool.to_int(databody[32:36])#高度
        speed=jctool.to_int(databody[36:40])*10#gps速度
        direction=jctool.to_int(databody[40:44])#方向
        time=databody[44:56]#gps时间
        #uploadtime="20"+gpsTime[0:2]+"-"+gpsTime[2:4]+"-"+gpsTime[4:6]+" "+gpsTime[6:8]+":"+gpsTime[8:10]+":"+gpsTime[10:]
        msgBody={"alarm":alarm,"status":status,"originalLatitude":originalLatitude,"originalLongitude":originalLongitude,
                 "speed":speed,"direction":direction,"time":time}
        return msgBody

