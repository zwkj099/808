# -*- coding: utf-8 -*-
'''
Created on 2019��8��19��

@author: admin
'''
import datetime
import time
from comman.autoupload import readexcel

def upload(tp,link,mobile,pdict,ex808dict,sensordict,info,extrainfo_id,idlist,wsid,excellist,tal=0):
    zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys = info
    date = datetime.datetime.strptime(pdict['detester'], "%Y-%m-%d %H:%M:%S")
    # date1 =datetime.datetime.strptime((date + datetime.timedelta(seconds=int(tal))).strftime("%y%m%d%H%M%S"), "%Y-%m-%d %H:%M:%S")
    date =date + datetime.timedelta(seconds=int(tal))
    second = 30
    timelist = []

    num = int(excellist[5])+1
    alarm_num = int(excellist[2])
    #主动安全数据
    zds[1]=excellist[1]  #事件

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

        sensordict['AD'] += 1
        sensordict['Oil'] += 1
        pdict['high'] += 1
        pdict['jin'] +=0.001
        pdict['wei'] +=0.001

        #如果报警事件需要改变
        if excellist[-2]=='yes':
            zds[1]+=1
            if ( zds[1] == 9):
                zds[1] = 16
            elif ( zds[1] == 19):
                zds[1] = 1

        #如果速度需要改变
        if excellist[-1]=='yes' and pdict['speed']<120:
            pdict['speed'] += 1
        else:
            pdict['speed']==5

        #如果循环次数大于报警次数，报警归0，不上传报警
        if (j+1)>alarm_num:
            wsid=[0]
        print "报警："
        print wsid
        gpsdata = tp.position(mobile, pdict['messageid'], 2, 0, pdict['alarm'], pdict['status'], pdict['jin'], pdict['wei'], pdict['high'], \
                              pdict['speed'], timelist[j], pdict['direction'],tp.extra_info(extrainfo_id, extrainfos), tp.zd_body(wsid, zds,timelist[j]),\
                              tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys), pdict['version'])

        gpshead = tp.data_head(mobile, pdict['messageid'], gpsdata, 3, pdict['version'])
        gpsdata = tp.add_all(gpshead + gpsdata)

        print "补传数据"
        tp.send_data(link, gpsdata)
        #如果循环次数小于等于里程需要增加的次数，里程每次加1，否则里程保持不变
        if (j+1) <num:
            print "里程："
            print extrainfos[4]
            extrainfos[4] += 1
        time.sleep(3)

def deal_data(pdict,zds,extrainfos,wsid1,i):
    for k in range(i, i + 1):
        excel_list = readexcel()
        if str(excel_list[k][0]).find('|') != -1:
            # wsid1 = list(map(lambda x: int(x), list(str(excel_list[k][0]).split('|'))))
            wslist = str(excel_list[k][0]).split('|')
            for m in wslist:
                wsid1.append(int(m))
        else:
            wsid1.append(int(excel_list[k][0]))
        zds[1] = int(excel_list[k][1])
        pdict['speed'] = int(excel_list[k][3])
        extrainfos[4] = excel_list[k][4]

    return [pdict,zds,extrainfos,wsid1,excel_list[k]]




