# -*- coding: utf-8 -*-

'''
Created on 2019-8-18

@author: Administrator
'''
import re
class read_configfile(object):
    
    def __init__(self):
        pass
    def readtestfile(self):
        
        from xml.dom import minidom
        testfile = "./config/testconfig.xml"
        dom = minidom.parse(testfile)
        
        publicdict = {}
        sichuandict = {}
        ex808dict = {}
        sensordict = {}
        bluetoothdict = {}
       
       
        publiclist = dom.getElementsByTagName("plublicparameters")[0].getElementsByTagName("Key")
        pul = dom.getElementsByTagName("plublicparameters")[0]
        for i in range(len(publiclist)):
            keyp,valuep=pul.getElementsByTagName("Key")[i].childNodes[0].data.split('=')
            if re.findall(r'^\d+\.\d+$',valuep,re.I)!=[]:
                publicdict[keyp] = float(valuep)
                 
            elif re.findall(r'^\d+$',valuep,re.I)!=[]:
                publicdict[keyp] = int(valuep)
            else:
                publicdict[keyp] = valuep
      
        sichuanlist = dom.getElementsByTagName("sichuanparameters")[0].getElementsByTagName("Key")
        sichuan = dom.getElementsByTagName("sichuanparameters")[0]
        for j in range(len(sichuanlist)):
            keys,values=sichuan.getElementsByTagName("Key")[j].childNodes[0].data.split('=')
            if re.findall(r'^\d+\.\d+$',values,re.I)!=[]:
                sichuandict[keys] = float(values)
               
            elif re.findall(r'^\d+$',values,re.I)!=[]:
                sichuandict[keys] = int(values)
            else:
                sichuandict[keys] = values
                   
        ex808list = dom.getElementsByTagName("Extras808parameters")[0].getElementsByTagName("Key")
        ex_808 = dom.getElementsByTagName("Extras808parameters")[0]
        
        for k in range(len(ex808list)):
            keyx,valuex = ex_808.getElementsByTagName("Key")[k].childNodes[0].data.split('=')
            if re.findall(r'^\d+\.\d+$',valuex,re.I)!=[]:
                ex808dict[keyx] = float(valuex)
            elif re.findall(r'^\d+$',valuex,re.I)!=[]:
                ex808dict[keyx] = int(valuex)
                
            else:
                ex808dict[keyx] = valuex
                   
    
        sensorlist = dom.getElementsByTagName("sensorparameters")[0].getElementsByTagName("Key")
        sensor = dom.getElementsByTagName("sensorparameters")[0]
        for m in range(len(sensorlist)):
            keyl,valuel  = sensor.getElementsByTagName("Key")[m].childNodes[0].data.split('=')
            if re.findall(r'^\d+\.\d+$',valuel,re.I)!=[]:
                sensordict[keyl] = float(valuel)
            elif re.findall(r'^\d+$',valuel,re.I)!=[]:
                sensordict[keyl] = float(valuel)
            else:    
                sensordict[keyl] = valuel
            
    
        bluetoothlist = dom.getElementsByTagName("bluetoothparameters")[0].getElementsByTagName("Key")
        bluetooth = dom.getElementsByTagName("bluetoothparameters")[0]
        for n in range(len(bluetoothlist)):
            keyb,valueb   = bluetooth.getElementsByTagName("Key")[n].childNodes[0].data.split('=')
            if re.findall(r'^\d+\.\d+$',valueb,re.I)!=[]:
                bluetoothdict[keyb] = float(valueb)
            elif re.findall(r'^\d+$',valueb,re.I)!=[]:
                bluetoothdict[keyb] = int(valueb)
            else:
                bluetoothdict[keyb] = valueb
                
             
        return [publicdict,sichuandict,ex808dict,sensordict,bluetoothdict]
    
    def build_data(self,pdict,sichuandict,ex808dict,sensordict,bluetoothdict,deviceid):
        # 川冀标主动安全参数
        zds=[sichuandict['sign'],sichuandict['event'],sichuandict['level'],sichuandict['deviate'],sichuandict['road_sign'],sichuandict['fatigue'],\
             pdict['jin'], pdict['wei'],pdict['high'],pdict['speed'],sichuandict['zstatus'],deviceid,sichuandict['attach_Count']]
    
        # 808附加信息相关参数
        extrainfos=[ex808dict['vedio_alarm'], ex808dict['vedio_signal'], ex808dict['memery'], ex808dict['abnormal_driving'],\
                    ex808dict['mel'], ex808dict['oil'], ex808dict['extra_speed'], ex808dict['by'], ex808dict['wn']]
    
        #外设传感器相关参数
        oils=[sensordict['AD'],sensordict['Oil'],pdict['high'],sensordict['addoil']]#油量传感器参数
        wds = [sensordict['sign'],sensordict['temp'],sensordict['times'],sensordict['warn']]#温度传感器参数
        sds = [sensordict['sign'],sensordict['hum'],sensordict['times'],sensordict['warn']]#湿度传感器参数
        yhs =[sensordict['oilsp'],sensordict['oiltemp'],sensordict['tio'],sensordict['times']]#油耗传感器参数
        zfs =[sensordict['sign'],sensordict['zt'],sensordict['fx'],sensordict['xs'],sensordict['times'],sensordict['li'],sensordict['xtimes']]#正反转传感器参数
        zzs = [sensordict['sign'],sensordict['dw'],sensordict['zt'],sensordict['cs'],sensordict['zl'],sensordict['zzzl'],\
               sensordict['ad1'],sensordict['ad2'],sensordict['ad3']]#载重传感器参数
        
        gss = [sensordict['fs'],sensordict['zt'],sensordict['ztime'],sensordict['bd'],sensordict['sj']]#工时传感器参数
        lcs = [sensordict['mel'],sensordict['speed']]#里程传感器参数
    
        lys=[bluetoothdict['num'],bluetoothdict['UUID'],bluetoothdict['signal'],bluetoothdict['distance'],bluetoothdict['battery']] #蓝牙信标数据

        return [zds,extrainfos,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys]
