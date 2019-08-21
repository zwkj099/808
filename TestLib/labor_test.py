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
    #  选择传感器型号id list
    sensor_indexlist=[0,1,2]
#     sensor_indexlist=[4]
    for key,value in info.items():
        for sensor_index in sensor_indexlist:#遍历三种工时测试
            #设置参数，并获取界面参数
            time.sleep(3)
            sensor_data = app.set_labor_parameter(value,browser,sensor_index,i,vnum,logfile,logtofile)
            time.sleep(8)
            #下发参数
            app.send_labor_parameter(browser,logfile,logtofile)
            
            #获取原始数据，下发的是8103,8900    
            reslist = response.getres(tp,link,mobile,["8103"],logfile,logtofile)
            i = i+1
            
            for res in reslist:
                result = False
                if res[2:6]=="8103":#解析数据
                    #数据算法，从0开始，到结束位+1
                    #说明：字典key值不能重复 [86-90,float,0.1]表示要转为浮点数，先乘以0.1再保留1位小数
#                     data_dic={"F3_id":["32-34","hex"],"外设ID":["34-36","hex"],"数据长度 ":["36-38"],"补偿使能":["38-42"],"滤波方式":["42-46"],"自动上传时间 ":["46-50"],\
#                                  "输出修正系数 K":["50-54"],"输出修正常数 B":["54-58"],"保留项1 ":["58-82"],"工时检测方式 ":["82-86"],"阈值 ":["86-90","float",0.1], \
#                                  "波动计算个数":["90-92"],"波动计算时间段":["92-94"],"平滑参数":["94-96"],"状态变换持续时长":["96-98"],"保留项2":["98-150"]}
                    
                    #解析原始数据
                    data_list =[(26,28,"hex"),(32,34,"hex"),(34,36,"hex"),(36,38,"hex"),(38,42),(42,46),(46,50),(50,54),(54,58),(58,82),(82,86),(86,90,"float",0.1),\
                                (90,92),(92,94),(94,96),(96,98),(98,150)]
                    #获取解析后的值
                    rdata = app.data_convert(data_list,res)
                    
                    #看界面获取的值是汉字还是数值，根据情况转换
                    compensate_dic={1:"使能",2:"禁用"}
                    filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}     
                    detectionmode_dic={0:"电压比较式",1:"油耗阈值式",2:"油耗波动式"}      
                    
                    if len(sensor_data)==8:#油耗阈值式
                        data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"工时检测方式",u"状态变换持续时长"]
                        send_data=[154,"01","F3","80","38",sensor_data[3],sensor_data[2],sensor_data[4],sensor_data[7]]
                        rec_data =[len(res),rdata[0],rdata[1],rdata[2],rdata[3],compensate_dic[rdata[4]],filterfactor_dic[rdata[5]],detectionmode_dic[rdata[10]],rdata[15]] 
                        
                    elif len(sensor_data)==9:#电压比较式 
                        data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"工时检测方式",u"状态变换持续时长",u"阈值,即电压值"]
                        send_data=[154,"01","F3","80","38",sensor_data[3],sensor_data[2],sensor_data[4],sensor_data[7],sensor_data[-1]]
                        rec_data =[len(res),rdata[0],rdata[1],rdata[2],rdata[3],compensate_dic[rdata[4]],filterfactor_dic[rdata[5]],detectionmode_dic[rdata[10]],rdata[15],str(rdata[11])]
#                          sensor_data=[plate_number,sensor_type,filterfactor,compensate,detectionMode,oddEvenCheck,baudrate,lastTimeYa,thresholdVoltage1] 
                    else:#油耗波动
                        
                        data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"滤波方式",u"补偿使能",u"工时检测方式",u"状态变换持续时长",\
                            u"波动计算个数",u"平滑参数",u"波动计算时间段"] 
                        send_data=[154,"01","F3","80","38"]

                        for i in range(len(sensor_data)):
                            if i not in [0,1,5,6,10,12]:#界面上的奇偶校验、波特率、波动阈值、速度阈值在协议中没有，无法比较
                                send_data.append(sensor_data[i])

                        rec_data =[len(res),rdata[0],rdata[1],rdata[2],rdata[3],filterfactor_dic[rdata[5]],compensate_dic[rdata[4]],detectionmode_dic[rdata[10]],rdata[15],rdata[-5],rdata[-3],rdata[-4]]

#                             sensor_data=[plate_number,sensor_type,filterfactor,compensate,detectionMode,oddEvenCheck,baudrate,lastTimeYa]
#                             valuelist =['baudRateCalculateNumber','smoothingFactor','baudRateThreshold','baudRateCalculateTimeScope','speedThreshold']

                #数据比对，返回结果True or False
                result = app.data_comparison(send_data,rec_data,data_title,logfile,logtofile) 
                    
                if result==True:
    #                 win32api.MessageBox(0, "polling test pass", "OK",win32con.MB_OK)
                    print "Labor test pass"
                    logtofile(logfile,"labor test pass\n")
                else:
                    logtofile(logfile,"labor test fail\n")
#                     win32api.MessageBox(0, "Labor test fail", "Fail",win32con.MB_ICONWARNING)
                    print "Labor test fail"
#     browser.quit()

def readconfig(sensordict):
    from xml.dom import minidom
    bfail = False
    if os.path.exists("./appconfig/labor.xml") == True:
        try:
            dom = minidom.parse("./appconfig/labor.xml")
            supportpdtlst =  dom.getElementsByTagName("SuportParameterList")[0].getElementsByTagName("Parameter")
            for snpninfo in supportpdtlst:
                lasttimethreshold = snpninfo.getElementsByTagName("lasttimethreshold")[0].childNodes[0].data
                Wavecalculatio_number = snpninfo.getElementsByTagName("Wavecalculatio_number")[0].childNodes[0].data
                smoothingFactor = snpninfo.getElementsByTagName("smoothingFactor")[0].childNodes[0].data
                baudRateThreshold = snpninfo.getElementsByTagName("baudRateThreshold")[0].childNodes[0].data
                Wavecalculatio_time = snpninfo.getElementsByTagName("Wavecalculatio_time")[0].childNodes[0].data
                speedThreshold = snpninfo.getElementsByTagName("speedThreshold")[0].childNodes[0].data
                thresholdVoltage = snpninfo.getElementsByTagName("thresholdVoltage")[0].childNodes[0].data                
                sensordict[1] = (lasttimethreshold,Wavecalculatio_number,smoothingFactor,baudRateThreshold,Wavecalculatio_time,speedThreshold,thresholdVoltage)
        except Exception as e:
            print "error config:"
            print e
        
    return sensordict
                    
                    
    