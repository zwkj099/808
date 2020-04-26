# -*- coding: utf-8 -*-
'''
Created on 2019年8月19日

@author: admin
'''
import time
###########  分包 ############
def subpackage(tp,link,mobile,gpsdata,version,messageid):
    '''
    消息最多发送长度为1024个字节，即2048个字符
消息体以外的内容长度：
    (2013-808)标识位+消息头+校验码+标识位 长度为38字符
    (2019-808)标识位+消息头+校验码+标识位 长度为48字符
消息体最大长度:
    2013-808只能为2048-38=2010字符,故消息体大于2010需要分包
    2019-808只能为2048-48=2000字符,故消息体大于2000需要分包
    '''
    gpsbody =[]
    size=2010 #默认消息体最长为2010
    if version==1:#当协议版本为808-2019时，将消息体最长改为2000
        size=2000

    if len(gpsdata)>size:
        if len(gpsdata)%size==0:
            count = (len(gpsdata)/size)
        else:
            count = (len(gpsdata)/size)+1
        for j in range(0,count):
            if len(gpsdata)>size:
                gpsbody.append(gpsdata[:size])
                gpsdata=gpsdata[size:]
            else:
                gpsbody.append(gpsdata)

    if gpsbody!=[]:
        print "需要分包："
        for i in range(len(gpsbody)):
            gpshead = tp.data_head(mobile, messageid,gpsbody[i] ,3,version,i,count)##将第几个分包、分包总数传给消息头
            gpsdata1 = tp.add_all(gpshead + gpsbody[i])
            print "分包："+str(i+1)
            tp.send_data(link, gpsdata1)

    ##########不分包 ###############
    else:
        gpshead = tp.data_head(mobile, messageid, gpsdata, 3, version)
        gpsdata = tp.add_all(gpshead + gpsdata)
        tp.send_data(link, gpsdata)

def location(tp, link, mobile,pdict, sichuandict, ex808dict, sensordict,bluetoothdict, extrainfo_id, idlist, wsid,deviceid,port, answer_number=0000):

    ########## 第三个参数说明要上传的位置条数,第四个为位置数据类型 ：0：正常位置批量汇报，1：盲区补报##########
    gpsdata = tp.position(mobile, pdict['messageid'], 2, 0, pdict['alarm'], pdict['status'], pdict['jin'], pdict['wei'],\
                          pdict['high'], pdict['speed'], pdict['ti'], pdict['direction'], \
                          tp.extra_info(extrainfo_id,ex808dict),tp.zd_body(wsid,pdict,sichuandict,deviceid,port),tp.f3_attach(idlist,pdict,sensordict,bluetoothdict), pdict['version'],answer_number)
    subpackage(tp, link, mobile,gpsdata,pdict['version'],pdict['messageid'])

def initial(tp, link, deviceid, vnum, mobile, version):
    # 注册
    data = tp.data_zc_body(deviceid, vnum, version)
    zchead = tp.data_head(mobile, 256, data, 1, version)
    data = tp.add_all((zchead + data))
    tp.send_data(link, data)
    time.sleep(1)
    Acode = tp.receive_data(link)  # 0：成功；1：车辆已被注册；2：数据库中无该车辆；3：终端已被注册；4：数据库中无该终端
    # Acode = "7E 81 00 00 13 01 99 66 66 00 01 00 02 00 01 00 37 66 62 34 64 66 39 62 62 38 64 62 34 31 32 35 08 7E" #直接使用平台返回的鉴权应答

    # 鉴权
    jqbody = tp.data_jq_body(Acode, version)
    jqhead = tp.data_head(mobile, 258, jqbody, 2, version)
    jqdata = tp.add_all((jqhead + jqbody))
    tp.send_data(link, jqdata)
    time.sleep(1)
    jqres = tp.receive_data(link)
    # 发送心跳数据
    heartdata = tp.heartbeat(mobile, version)
    tp.send_data(link, heartdata)