# -*- coding: utf-8 -*-
import xlrd
import time
import testlibrary
import re
import datetime
import reply
from config import readconfig
from comman import upload_location, reply_position
readcig = readconfig()
tp = testlibrary.testlibrary()

"""
   传感器报表：除了I/O报表、胎压报表、OBD行程报表、油量里程报表（上面跑完会有数据）、F3高精度报表

"""
def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    datalist = readexcel()
    keylist =[]
    start_value=[]
    change_value=[]
    max_value=[]

    ##设置初始值
    for data in datalist:
        keylist.append(data[1])
        start_value.append(data[2])
        change_value.append(data[3])
        max_value.append(data[4])

    for m in range(len(keylist)):
        if re.findall(r'^\d+\.\d+$', str(start_value[m]), re.I) != []:
            sensordict[keylist[m]] = float(start_value[m])
        else:
            sensordict[keylist[m]]=int(start_value[m])

    #初始值完后上传一次位置
    upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                             extrainfo_id, idlist, wsid, deviceid, port)

    # print sensordict
    # 控制第x次通用应答响应
    x = 0
    k = 1
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))
        if k>20:
            print "######### 传感器报表数据准备完成 #######"
            break

        while True:
            if k>20:
                break

            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                pdict['jin'] += 0.001
                pdict['wei'] += 0.001
                n=0

                ##变化值
                for n in range(len(keylist)):
                    if max_value[n]=='':
                        sensordict[keylist[n]]+=int(change_value[n])
                    elif sensordict[keylist[n]]<int(max_value[n]):
                        sensordict[keylist[n]] += int(change_value[n])
                    else:
                        if re.findall(r'^\d+\.\d+$',str(start_value[n]),re.I)!=[]:
                            sensordict[keylist[n]] = float(start_value[n])
                        else:
                            sensordict[keylist[n]] = int(start_value[n])

                upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                         extrainfo_id, idlist, wsid, deviceid, port)
                k += 1
                res = tp.receive_data(link)
                res = tp.dd(res)
                # 切割响应
                list = ano_res(res)
                # 判断响应并根据响应id回复
                for j in list:
                    # 根据下发报文判断需要响应内容
                    id = res[2:6]
                    # 应答流水号
                    if pdict['version']==0:
                        answer_number = res[22:26]
                    elif pdict['version']==1:
                        answer_number = res[32:36]
                    reno = "00"
                    if id in ["8201", "8202","8802","8500"]:
                        reply_position.reply_pos(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict,
                                                 bluetoothdict, extrainfo_id,
                                                 idlist, wsid, deviceid, port, answer_number, res, id, reno)

                    else:
                        reply.reply(tp,link, res, mobile, id, answer_number, reno,pdict['version'])

                t = int(time.strftime("%H%M%S", time.localtime()))
            else:
                try:
                    reno = "00"
                    res = tp.receive_data(link)
                    res = tp.dd(res)
                    id = res[2:6]
                    # 应答流水号
                    if pdict['version']==0:
                        answer_number = res[22:26]
                    elif pdict['version']==1:
                        answer_number = res[32:36]
                    # 切割响应
                    #list=ano_res(res)
                    if id in ["8201", "8202","8802","8500"]:
                        try:
                            reply_position.reply_pos(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict,
                                                     bluetoothdict, extrainfo_id,
                                                     idlist, wsid, deviceid, port, answer_number, res, id, reno)
                        except Exception as e:
                            print e
                    else:
                        reply.reply(tp,link, res, mobile, id, answer_number, reno,pdict['version'])

                except:
                    pass

# 切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa = "7e.+7e"
    re_list = re.findall(pa, str(res))
    return re_list

def readexcel():
    file_path = r'./comman/upload.xlsx'
    # file_path = r'../../comman/upload.xlsx'
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[3]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    list = []
    for i in range(1,row_num):
        rowlist = []
        if data_sheet.cell_value(i, 1) != '':
            for j in range(col_num):
                valuex=data_sheet.cell_value(i, j)
                if re.findall(r'^\d+\.0$', str(valuex), re.I) != []:
                    rowlist.append(int(valuex))

                else:
                    rowlist.append(valuex)

        if rowlist!=[]:
            list.append(rowlist)
    return  list

# list = readexcel()
# print list