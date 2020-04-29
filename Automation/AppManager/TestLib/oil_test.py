# -*- coding: utf-8 -*-
'''
Created on 2019��7��8��

@author: admin
'''
import time
from comman.response_type import is_need_res
from comman.general_response import Usual,get_usyal_body
from nt import times
import os
import win32api
import win32con
from comman.response_0900 import Answer_0900
import re

def main(browser,args,testinfo,tp,link,app,mobile,vnum,logfile,logtofile):

    sensordict = {}
    info=readconfig(sensordict)
    i=0
    for key,value in info.items():
        #轮询下发
#         time.sleep(5)
#         [noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold]=sensor_data
        sensor_data,calibration = app.set_oil_parameter(value,browser,vnum,logfile,logtofile)
        time.sleep(8)
        
        app.send_oil_parameter(browser,logfile,logtofile)
        
        reslist=[]
        while True:
            try:
                ress = tp.receive_data(link)
                if ress[2:6] not in ["8103","8900"] and ress[2:6]!="":
                    logtofile(logfile,"receive data:"+tp.change_a(tp.dd(ress))+"\n")
                if len(reslist)==2:
                    break
                list1=[]
                if re.findall(r'7e7e',ress,re.I)!=[]:
                    list1 = ress.split('7e7e')
                    for j in range(len(list1)):
                        if j==0:
                            list1[0]+='7e'
                        elif j == len(reslist)-1:
                            list1[j] = '7e'+list1[j]
                        else:
                            list1[j] = '7e'+list1[j]+'7e'
                else:
                    list1.append(ress)
                        
                print list1
                
#                 list=re.findall(r'(7e.*?7e)', ress)
                for res in list1:
                    #数据比对
                    res = tp.dd(res)
#                     print "res:"
#                     print res
                    logtofile(logfile,"receive data:"+tp.change_a(res)+"\n")
                    if res[2:6] in ["8103","8900"]:
                        reslist.append(res)
                    # 应答
    #                 time.sleep(3)
                    
                    id = res[2:6]
                    answer_number = res[22:26]  # 应答流水号
                    reno = "00"
                    # 平台下发指令8900
                    if is_need_res(res) == 6:
                        print "receive 8900"
                        Usualdata =Usual(link, mobile, id, answer_number, reno)  # 应答通用应答  
                        answerdata = Answer_0900(link, mobile, res[34:36], answer_number, reno)  # 应答0900 
                        print "8900"
                        logtofile(logfile,"send data:"+Usualdata+"\n")
                        logtofile(logfile,"send data:"+answerdata+"\n")
                    # 平台下发指令8103
                    elif is_need_res(res) == 7:
                        print "receive 8103"
                        Usualdata =Usual(link, mobile, id, answer_number,reno)  # 应答通用应答
                        logtofile(logfile,"send data:"+Usualdata+"\n")
                        if tp.to_int(res[28:34])==243: # 获取设置的ID，如果是带F3的ID，则通用应答后需要继续应答0900
                            answerdata =Answer_0900(link,mobile, res[34:36], answer_number, reno)
                            print "8103"
                            logtofile(logfile,"send data:"+answerdata+"\n")
                    else:
                        pass
                    
                    i = i+1    
#                 time.sleep(5) 
            except:
                pass

        for res in reslist:
            result = app.oil_compare(sensor_data,calibration,res,mobile,logfile,logtofile)
            if result==True:
#                 win32api.MessageBox(0, "polling test pass", "OK",win32con.MB_OK)
                print "Oil test pass"
                logtofile(logfile,"oil test pass\n")
            else:
                logtofile(logfile,"oil test fail\n")
#                 win32api.MessageBox(0, "oil test fail", "Fail",win32con.MB_ICONWARNING)
                print "Oil test fail"
#     browser.quit()

def readconfig(sensordict):
    from xml.dom import minidom
    bfail = False
    if os.path.exists("./Automation/AppManager/appconfig/oil.xml") == True:
        try:
            dom = minidom.parse("./Automation/AppManager/appconfig/oil.xml")
            supportpdtlst =  dom.getElementsByTagName("SuportParameterList")[0].getElementsByTagName("Parameter")
            for snpninfo in supportpdtlst:
                group_num = snpninfo.getElementsByTagName("group_num")[0].childNodes[0].data
                autouploadtime = snpninfo.getElementsByTagName("autouploadtime")[0].childNodes[0].data
                output_k = snpninfo.getElementsByTagName("output_k")[0].childNodes[0].data
                output_b = snpninfo.getElementsByTagName("output_b")[0].childNodes[0].data
                addoiltime = snpninfo.getElementsByTagName("addoiltime")[0].childNodes[0].data
                addoil = snpninfo.getElementsByTagName("addoil")[0].childNodes[0].data
                seepoiltime = snpninfo.getElementsByTagName("seepoiltime")[0].childNodes[0].data
                seepoil = snpninfo.getElementsByTagName("seepoil")[0].childNodes[0].data
                
                sensordict[group_num] = (group_num,autouploadtime,output_k,output_b,addoiltime,addoil,seepoiltime,seepoil)
        except Exception as e:
            print "error config:"
            print e
                
    return sensordict
                    
                    
    