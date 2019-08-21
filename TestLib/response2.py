# -*- coding: utf-8 -*-
'''
Created on 2019��7��24��

@author: admin
'''
from comman.response_type import is_need_res
from comman.general_response import Usual,get_usyal_body
from comman.response_0900 import Answer_0900
import re

def getres(tp,link,mobile,cmdlist,logfile,logtofile):
    reslist=[]
    while True:
        try:

            ress = tp.receive_data(link)
            if ress[2:6] not in cmdlist:
                logtofile(logfile,"receive data:"+tp.change_a(tp.dd(ress))+"\n")
            if len(reslist)==len(cmdlist):
                break 
            list1=[]
            if re.findall(r'7e7e',ress,re.I)!=[]:
                list1.append(re.findall(r'(7e.*7e)7e',ress,re.I)[0])
                list1.append(re.findall(r'7e(7e.*7e)',ress,re.I)[0])
        
            else:
                list1.append(ress)              

            for res in list1:
                #数据比对
                res = tp.dd(res)

                logtofile(logfile,"receive data:"+tp.change_a(res)+"\n")
                if res[2:6] in cmdlist:
                    reslist.append(res)
                
                id = res[2:6]
                answer_number = res[22:26]  # 应答流水号
                reno = "00"
                # 平台下发指令8900
                if is_need_res(res) == 6:
                    Usualdata =Usual(link, mobile, id, answer_number, reno)  # 应答通用应答  
                    answerdata = Answer_0900(link, mobile, res[34:36], answer_number, reno)  # 应答0900 
                    logtofile(logfile,"send data:"+Usualdata+"\n")
                    logtofile(logfile,"send data:"+answerdata+"\n")
                # 平台下发指令8103
                elif is_need_res(res) == 7:
                    Usualdata =Usual(link, mobile, id, answer_number,reno)  # 应答通用应答
                    logtofile(logfile,"send data:"+Usualdata+"\n")
                    if tp.to_int(res[28:34])==243: # 获取设置的ID，如果是带F3的ID，则通用应答后需要继续应答0900
                        answerdata =Answer_0900(link,mobile, res[34:36], answer_number, reno)
                        logtofile(logfile,"send data:"+answerdata+"\n")
                else:
                    pass
                   
#                 time.sleep(5) 
        except:
            pass   
        
    return reslist 