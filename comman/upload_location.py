# -*- coding: utf-8 -*-
'''
Created on 2019年8月19日

@author: admin
'''
import time
def location(tp,link,mobile,pdict,ex808dict,sensordict,info,extrainfo_id,idlist,wsid,answer_number=0000):
    
    zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys = info
    gpsdata = tp.position(mobile, pdict['messageid'], 6, 1, pdict['alarm'], pdict['status'], pdict['jin'], pdict['wei'],\
                          pdict['high'], pdict['speed'], pdict['ti'], pdict['direction'], \
                          tp.extra_info(extrainfo_id,extrainfos),tp.zd_body(wsid,zds),tp.f3_attach(idlist,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys), pdict['version'],answer_number)
    gpshead = tp.data_head(mobile, pdict['messageid'], gpsdata, 3, pdict['version'])
    gpsdata = tp.add_all(gpshead + gpsdata)
    tp.send_data(link, gpsdata)


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