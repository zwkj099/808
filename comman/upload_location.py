# -*- coding: utf-8 -*-
'''
Created on 2019年8月19日

@author: admin
'''
def location(tp,link,mobile,pdict,ex808dict,sensordict,info,extrainfo_id,idlist,wsid,answer_number=0000):
    
    zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys = info
    gpsdata = tp.position(mobile, pdict['messageid'], 2, 1, pdict['alarm'], pdict['status'], pdict['jin'], pdict['wei'],\
                          pdict['high'], pdict['speed'], pdict['ti'], pdict['direction'], \
                          tp.extra_info(extrainfo_id,extrainfos),tp.zd_body(wsid,zds),tp.f3_attach(idlist,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys), pdict['version'],answer_number)
    tp.send_data(link, gpsdata)
#     return tp
