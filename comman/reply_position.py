# -*- coding: utf-8 -*-
'''
Created on 2019年8月19日

@author: admin
'''
import upload_location
import time

def reply_pos(tp,link,mobile,pdict,sichuandict, ex808dict, sensordict,bluetoothdict,extrainfo_id,idlist,wsid, deviceid, port,answer_number,res,id,reno):
    
#     zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys = info
    
    # 平台下发指令8201，位置信息查询
    if id == "8201":
        sensordict['AD'] += 1  # 增加油量传感器－ＡＤ值
        sensordict['Oil'] += 1  # 增加油量传感器－油量
        pdict['high'] += 1  # 增加油量传感器－高度
        ex808dict['mel'] += 1  # 增加－里程

        pdict['alarm']=2147483647
        pdict['messageid']=513
        # upload_location.location(tp,link,mobile,pdict,extrainfos,zds,info,extrainfo_id,idlist,wsid,answer_number)# 组装0201位置数据，包含油量数据、里程数据
        upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                 extrainfo_id, idlist, wsid, deviceid, port,answer_number)
        pdict['messageid']=512
        pdict['alarm']=0
    # 平台下发指令8202,跟踪
    elif id == "8202":
        nu = tp.to_int(res[26:30])  # 获取回传间隔时间
        tim = tp.to_int(res[30:38])  # 获取跟踪有效时长
        print answer_number, nu, tim
        # 应答通用应答
        import sys
        sys.path.append("..")
        import reply
        usual_body = reply.get_usyal_body(id, answer_number, reno)
        usual_head = tp.data_head(mobile, 1, usual_body, 5)
        usual_redata = tp.add_all(usual_head + usual_body)
        # tp.send_data(link, usual_redata)
        #reply.reply(link, res, mobile, id, answer_number, reno)
        i = 0
        while i < tim / nu:
            # 组装0200位置数据，包含油量数据、里程数据
            tp.send_data(link, usual_redata)
            upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                     extrainfo_id, idlist, wsid, deviceid, port, answer_number)
            time.sleep(nu)
            i += 1
            print "第%d次发送跟踪信息：" % i
    elif id == "8802":#存储多媒体数据检索
        pdict['messageid'] = 2050
        upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                 extrainfo_id, idlist, wsid, deviceid, port, answer_number)
        pdict['messageid'] = 512
    elif id == "8500":#终端控制－加解锁
        pdict['messageid'] = 1280
        upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                 extrainfo_id, idlist, wsid, deviceid, port, answer_number)
        pdict['messageid'] = 512