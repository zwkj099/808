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
    只上传终端里程报表、行驶报表、停止报表
    起始里程	总里程	行驶里程	怠速里程	异常里程	行驶时长	油耗	行驶次数	停止次数	停止时长
    上传100条数据

"""
def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    ex808dict['mel']=100
    pdict['speed']=80
    sensordict['oilsp']=10

    print "######### 开始上传位置报表数据 #######"

    # 控制第x次通用应答响应
    x = 0
    k = 0
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))

        if k>100:
            print "######### 位置报表数据准备完成 #######"
            break
        while True:
            if k>100:
                break
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                if k<10:
                    sensordict['tio'] += 10
                    sensordict['oilsp']+=2
                    pdict['speed'] += 1
                    ex808dict['mel'] += 1
                elif k > 10 and k < 20:  # 怠速
                    sensordict['tio'] += 2
                    sensordict['oilsp'] += 1
                    pdict['speed'] = 4
                    ex808dict['mel'] += 1

                elif k > 20 and k < 30:  # 行驶
                    if k == 21:
                        pdict['speed'] = 50
                    sensordict['tio'] += 10
                    sensordict['oilsp'] += 2
                    pdict['speed'] += 1
                    ex808dict['mel'] += 1
                elif k > 40 and k < 50:  #怠速
                    sensordict['tio'] += 2
                    sensordict['oilsp'] += 1
                    pdict['speed'] = 3
                    ex808dict['mel'] += 1

                elif k > 50 and k < 60:  # 行驶
                    if k == 51:
                        pdict['speed'] = 30
                    sensordict['tio'] += 10
                    sensordict['oilsp'] += 2
                    pdict['speed'] += 1
                    ex808dict['mel'] += 1
                elif k > 60 and k < 70:  # 怠速
                    sensordict['tio'] += 2
                    sensordict['oilsp'] += 1
                    pdict['speed'] = 3
                    ex808dict['mel'] += 1
                elif k > 70 and k < 80:  # 行驶
                    if k == 71:
                        pdict['speed'] = 30
                    sensordict['tio'] += 10
                    sensordict['oilsp'] += 2
                    pdict['speed'] += 1
                    ex808dict['mel'] += 1



                pdict['high'] += 1
                pdict['jin'] += 0.001
                pdict['wei'] += 0.001

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

# def readexcel():
#     file_path = r'./comman/upload.xlsx'
#     workbook = xlrd.open_workbook(file_path)
#     data_sheet = workbook.sheets()[2]
#     row_num = data_sheet.nrows
#     col_num = data_sheet.ncols
#
#     list = []
#     for i in range(1,row_num):
#         rowlist = []
#         if data_sheet.cell_value(i, 1) != '':
#             for j in range(col_num):
#
#                     if isinstance(data_sheet.cell_value(i, j),float):
#                         rowlist.append(int(data_sheet.cell_value(i, j)))
#                     else:
#                         rowlist.append(data_sheet.cell_value(i, j))
#         if rowlist!=[]:
#             list.append(rowlist)
#     return  list