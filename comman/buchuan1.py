# -*- coding: utf-8 -*-
'''
Created on 2019��8��19��

@author: admin
'''
from comman import upload_location
import datetime
import time
from comman.autoupload import readexcel

def upload(tp,link,mobile, pdict, sichuandict, ex808dict, sensordict,bluetoothdict,extrainfo_id,idlist,wsid,excellist,deviceid,port=6975,tal=0,answer_number=0000):
    date = datetime.datetime.strptime(pdict['detester'], "%Y-%m-%d %H:%M:%S")
    # date1 =datetime.datetime.strptime((date + datetime.timedelta(seconds=int(tal))).strftime("%y%m%d%H%M%S"), "%Y-%m-%d %H:%M:%S")
    date =date + datetime.timedelta(seconds=int(tal))
    second = 30
    timelist = []
    num = int(excellist[5])+1
    alarm_num = int(excellist[2])
    #主动安全数据
    sichuandict['event']=excellist[1]  #事件

    cycle_index = 0
    if num > alarm_num:
        cycle_index=num
    else:
        cycle_index = alarm_num

    for i in range(0,cycle_index):#120表示1小时
        time1 = (date + datetime.timedelta(seconds=second)).strftime("%y%m%d%H%M%S")
        timelist.append(time1)
        second += 30

    ll = 0
    # for j in range(0, len(timelist)):
    print "循环次数： "+ str(cycle_index)
    for j in range(0,cycle_index):

        sensordict['AD'] += 1  # 增加油量传感器ＡＤ值
        sensordict['Oil'] += 1  # 增加油量传感器油量值
        pdict['high'] += 1
        pdict['jin'] +=0.001
        pdict['wei'] +=0.001

        #如果报警事件需要改变
        if excellist[-2]=='yes':
            sichuandict['event']+=1
            if ( sichuandict['event'] == 9):
                sichuandict['event'] = 16
            elif ( sichuandict['event'] == 19):
                sichuandict['event'] = 1

        #如果速度需要改变
        if excellist[-1]=='yes' and pdict['speed']<120:
            pdict['speed'] += 1
        else:
            pdict['speed']==5

        #如果循环次数大于报警次数，报警归0，不上传报警
        if (j+1)>alarm_num:
            wsid=[0]
        gpsdata = tp.position(mobile, pdict['messageid'], 6, 1, pdict['alarm'], pdict['status'], pdict['jin'],
                              pdict['wei'], \
                              pdict['high'], pdict['speed'], timelist[j], pdict['direction'], \
                              tp.extra_info(extrainfo_id, ex808dict),
                              tp.zd_body(wsid, pdict, sichuandict, deviceid, port),
                              tp.f3_attach(idlist, pdict, sensordict, bluetoothdict), pdict['version'], answer_number) #组装位置消息体，用timelist[j]替换pdict['ti']
        upload_location.subpackage(tp, link, mobile, gpsdata, pdict['version'], pdict['messageid'])#断定是否分包发送，并组装消息头消息体再发送数据

        #如果循环次数小于等于里程需要增加的次数，里程每次加1，否则里程保持不变
        if (j+1) <num:
            print "里程："
            print ex808dict['mel']
            ex808dict['mel'] += 1
        time.sleep(3)

def deal_data(pdict, sichuandict, ex808dict, sensordict,bluetoothdict,wsid1,i):
    for k in range(i, i + 1):
        excel_list = readexcel()#封装读取excel数据
        if str(excel_list[k][0]).find('|') != -1:
            # wsid1 = list(map(lambda x: int(x), list(str(excel_list[k][0]).split('|'))))
            wslist = str(excel_list[k][0]).split('|')
            for m in wslist:
                wsid1.append(int(m))
        else:
            wsid1.append(int(excel_list[k][0]))
            sichuandict['event'] = int(excel_list[k][1])
        pdict['speed'] = int(excel_list[k][3])
        ex808dict['mel'] = excel_list[k][4]

    return [wsid1,excel_list[k]]




