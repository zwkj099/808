# -*- coding: utf-8 -*-
'''
Created on 2019��8��21��

@author: admin
'''
# import time
# def initial(tp,link,deviceid,vnum,mobile,version):
#     #注册
#     data=tp.register(deviceid,vnum,mobile,version )
#     tp.send_data(link,data)
#     time.sleep(1)
#     Acode=tp.receive_data(link) #0：成功；1：车辆已被注册；2：数据库中无该车辆；3：终端已被注册；4：数据库中无该终端
#     #Acode = "7E 81 00 00 13 01 99 66 66 00 01 00 02 00 01 00 37 66 62 34 64 66 39 62 62 38 64 62 34 31 32 35 08 7E" #直接使用平台返回的鉴权应答
#
#     #鉴权
#     jqdata=tp.Authentication(Acode,mobile,version)
#     tp.send_data(link,jqdata)
#     time.sleep(1)
#     jqres=tp.receive_data(link)
#     #发送心跳数据
#     heartdata = tp.heartbeat(mobile, version)
#     tp.send_data(link, heartdata)


