# -*- coding: utf-8 -*-
import xlrd
import time
import testlibrary
import re
import datetime
import reply
from config import readconfig
from comman import upload_location, reply_position,setMileage
readcig = readconfig()
tp = testlibrary.testlibrary()

"""
   四川监管报表：车辆异动统计
   （1）车辆管理中设置车辆为客车
   （2）在报警设置平台报警中设四川标准的异动报警
   下面上传的是车辆异动报警
    目前没有触发车辆异动报警
"""
def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    # 设置redis里程，传入车辆id，公共参数pdict
    setMileage.setto_redismel(vehicle_id, ex808dict, pdict['redishost'], pdict['db'], pdict['pwd'])
    datalist = readexcel()

    maxspeed = datalist[0][1]
    lasttime = datalist[1][1]

    pdict['speed']=maxspeed
    tt= int(time.strftime("%H%M%S", time.localtime()))
    #初始值完后上传一次位置
    upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                             extrainfo_id, idlist, wsid, deviceid, port)

    # print sensordict
    # 控制第x次通用应答响应
    x = 0
    kk=0
    isover = False
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))
        if isover==True:
            print "######### 车辆异动统计数据准备完成 #######"
            break

        while True:
            # ##持续超速统计
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                if kk*pdict['period']>(int(lasttime) * 60):
                    isover = True
                    break

                pdict['jin'] += 0.001
                pdict['wei'] += 0.001
                ex808dict['mel'] += 0.5
                upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                         extrainfo_id, idlist, wsid, deviceid, port)
                kk += 1
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
    data_sheet = workbook.sheets()[5]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    list = []
    for i in range(5,row_num):
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