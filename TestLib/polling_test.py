# -*- coding: utf-8 -*-
'''
Created on 2019��7��8��

@author: admin
'''
import re
import time
from comman.response_type import is_need_res
from comman.general_response import Usual,get_usyal_body
from nt import times
import os
import win32api
import win32con



def main(browser,args,testinfo,tp,link,app,mobile,vnum,logfile,logtofile):

    sensordict = {}
    info=readconfig(sensordict)
    i=0
    for key,value in info.items():
        #轮询下发
        time.sleep(5)
        plate_number, sensor, timestr = app.set_polling_parameter(value[0],browser,value[1],i,vnum,logfile,logtofile)
        time.sleep(5)
        
        app.send_polling_parameter(browser,logfile,logtofile)
        res = tp.receive_data(link)
        #数据比对
        res = tp.dd(res)
#         print "接收数据："
#         print res
        if re.findall(r'7e7e',res,re.I)!=[]:
            reslist = res.split('7E7E')
            for j in range(len(reslist)):
                if j==0:
                    reslist[0]+='7E'
                elif j == len(reslist)-1:
                    reslist[j] = '7E'+reslist[j]
                else:
                    reslist[j] = '7E'+reslist[j]+'7E'
        else:
            reslist.append(res)

                
        print "reslist"
        print reslist
        for rex in reslist:
            logtofile(logfile,"receive data:"+tp.change_a(rex)+"\n")
            if rex[2:6]=='8900':
                res = rex
        result = app.poling_compare([plate_number, sensor, timestr],res,mobile,logfile,logtofile)
        
       
        # 应答
        time.sleep(10)
        id = res[2:6]
        answer_number = res[22:26]  # 应答流水号
        reno = "00"
        if is_need_res(res) == 6:
            Usualdata = Usual(link, mobile, id, answer_number, reno)  # 应答通用应答  
            logtofile(logfile,"send data:"+Usualdata+"\n") 
        if result==True:
#             win32api.MessageBox(0, "polling test pass", "OK",win32con.MB_OK)
            print "polling test pass"
            logtofile(logfile,"polling test pass\n")
        else:
            logtofile(logfile,"polling test fail\n")
#             win32api.MessageBox(0, "polling test fail", "Fail",win32con.MB_ICONWARNING)
            print "polling test fail"
            
        i = i+1
      
        time.sleep(5) 
#     browser.quit()

def readconfig(sensordict):
    from xml.dom import minidom
    bfail = False
    if os.path.exists("./appconfig/polling.xml") == True:
        try:
            dom = minidom.parse("./appconfig/polling.xml")
            supportpdtlst =  dom.getElementsByTagName("SuportParameterList")[0].getElementsByTagName("Parameter")
            for snpninfo in supportpdtlst:
                sensor = snpninfo.getElementsByTagName("sensor")[0].childNodes[0].data
                timestr = snpninfo.getElementsByTagName("timestr")[0].childNodes[0].data
                sensordict[sensor] = (sensor,timestr)
        except Exception as e:
            print e
                
    return sensordict
                    
                    
    