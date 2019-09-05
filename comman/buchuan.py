# -*- coding: utf-8 -*-
'''
Created on 2019��8��19��

@author: admin
'''
import datetime

def upload(tp,link,mobile,pdict,ex808dict,sensordict,info,extrainfo_id,idlist,wsid):
    zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys = info
    date = datetime.datetime.strptime(pdict['detester'], "%Y-%m-%d %H:%M:%S")
    second = 30
    timelist = []
    for i in range(0, 120):#120表示1小时
        time1 = (date + datetime.timedelta(seconds=second)).strftime("%y%m%d%H%M%S")
        timelist.append(time1)
        second += 30
 
    for j in range(0, len(timelist)):
        extrainfos[4] += 1
        sensordict['AD'] += 1
        sensordict['Oil'] += 1
        pdict['high'] += 1
        pdict['jin'] +=0.001
        pdict['wei'] +=0.001
        gpsdata = tp.position(mobile, pdict['messageid'], 2, 0, pdict['alarm'], pdict['status'], pdict['jin'], pdict['wei'], pdict['high'], \
                              pdict['speed'], timelist[j], pdict['direction'],tp.extra_info(extrainfo_id, extrainfos), tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys), pdict['version'])
        print "补传数据"
        tp.send_data(link, gpsdata)   