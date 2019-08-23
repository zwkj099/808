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
import response


def main(browser,args,testinfo,tp,link,app,mobile,vnum,logfile,logtofile):

    sensordict = {}
    info=readconfig(sensordict)
    i=0
    for key,value in info.items():
        
        #设置UI参数
        sensor_data,calibration = app.set_load_parameter(value,browser,i,vnum,logfile,logtofile)
        
        no,plate_number,sensor,baudrate,filterfactor,compensate,oddEvenCheck,loadMeterWay,loadMeterUnit,noLoadValue,\
            noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold=sensor_data
        time.sleep(8)
        
        #下发参数
        app.send_load_parameter(browser,logfile,logtofile)
        
        #获取原始数据，下发的是8103,8900,如果单个，就写["8103"]或者["8900"]   
        reslist = response.getres(tp,link,mobile,["8103","8900"],logfile,logtofile)
        i = i+1
        

        try:    
            for res in reslist:
                result = False
                if res[2:6]=="8103":#解析数据
                    #解析原始数据
                    
                    #1 数据长度 2 补偿使能 3 滤波方式 4自动上传时间 5输出修正系数 K 6输出修正常数 B 7保留项  8重量单位  9保留  10核定载荷重量 11超载阈值  12超载阈值偏差 13载重测量方案 
                    # 14满载阈值 15满载阈值偏差 16空载阈值  17空载阈值偏差 18轻载阈值  19轻载阈值偏差 20保留项 
                    #F3_id 外设id 数据长度
                    data_list =[(32,34,"hex"),(34,36,"hex"),\
                                (36,38,"hex"),(38,42),(42,46),(74,78),(94,98),(86,90),(90,94),(98,102),(102,106),\
                                (106,110),(110,114),(114,118),(118,122)]
                    #获取解析后的值
                    rec_data = app.data_convert(data_list,res)
                    
                    data_title=[u"消息总长度",u"透传消息类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"重量单位",u"载重测量方案",u"超载阈值",\
                          u"超载阈值偏差",u"满载阈值",u"满载阈值偏差",u"空载阈值",u"空载阈值偏差",u"轻载阈值",\
                          u"轻载阈值偏差"] 
                    rec_data.insert(0,len(res))
                    
                    compensate_dic={u"使能":1,u"禁用":2}
                    filterfactor_dic={u"实时":1,u"平滑":2,u"平稳":3} 
                    send_data=[154,"F3",no,"38",compensate_dic[compensate],filterfactor_dic[filterfactor],loadMeterUnit,loadMeterWay,overLoadValue,overLoadThreshold,fullLoadValue,\
                                           fullLoadThreshold,noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold]
                    
                    
                # u"透传消息类型",数据总包数，u"外设ID",u"数据长度",标定组数，
                
                if res[2:6]=="8900":
                    data_title=[u"透传消息类型",u"外设ID",u"消息包总数",u"标定组数"]
                    
                    data_list =[(26,28,"hex"),(30,32,"hex"),(28,30,"hex"),(32,34)]
                    j = 34
                    for n in range(len(calibration)):
                        data_list.append((j,j+8))
                        data_list.append((j+8,j+16,"float",1))
                        data_title.append(u"AD值")
                        data_title.append(u"车辆载荷重量")
                        j = j + 16
                        
                    rec_data=app.data_convert(data_list,res)
                    
                    send_data = ["F6",no,"01",len(calibration)+1]
                    for key,value in calibration.items():
                        send_data.append(value[0])
                        send_data.append(value[1])
     
    
                #数据比对，返回结果True or False
                result = app.data_comparison(send_data,rec_data,data_title,logfile,logtofile) 
            
                if result==True:
        #             win32api.MessageBox(0, "polling test pass", "OK",win32con.MB_OK)
                    print "load test pass"
                    logtofile(logfile,"load test pass\n")
                else:
                    logtofile(logfile,"load test fail\n")
    #                 win32api.MessageBox(0, "load test fail", "Fail",win32con.MB_ICONWARNING)
                    print "load test fail"
        
        except Exception as e:
            print e               
#     browser.quit()

def readconfig(sensordict):
    from xml.dom import minidom
    bfail = False
    if os.path.exists("./appconfig/load.xml") == True:
        try:
            dom = minidom.parse("./appconfig/load.xml")
            supportpdtlst =  dom.getElementsByTagName("SuportParameterList")[0].getElementsByTagName("Parameter")
            for snpninfo in supportpdtlst:
                no = snpninfo.getElementsByTagName("NO")[0].childNodes[0].data
                noLoadValue = snpninfo.getElementsByTagName("noLoadValue")[0].childNodes[0].data
                noLoadThreshold = snpninfo.getElementsByTagName("noLoadThreshold")[0].childNodes[0].data
                lightLoadValue = snpninfo.getElementsByTagName("lightLoadValue")[0].childNodes[0].data
                lightLoadThreshold = snpninfo.getElementsByTagName("lightLoadThreshold")[0].childNodes[0].data
                fullLoadValue = snpninfo.getElementsByTagName("fullLoadValue")[0].childNodes[0].data
                fullLoadThreshold = snpninfo.getElementsByTagName("fullLoadThreshold")[0].childNodes[0].data
                overLoadValue = snpninfo.getElementsByTagName("overLoadValue")[0].childNodes[0].data
                overLoadThreshold = snpninfo.getElementsByTagName("overLoadThreshold")[0].childNodes[0].data
                
                sensordict[no] = (noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold)
        except Exception as e:
            print "error config:"
            print e
                
    return sensordict
                    
                    
    