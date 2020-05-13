# -*- coding: utf-8 -*-

import time
import testlibrary
from config import readconfig
from comman import upload_location, reply_position
from Applet.redis_operation import setMileage
import xlrd
import reply
import re

readcig = readconfig()
tp = testlibrary.testlibrary()




'''
四川监管报表：疲劳驾驶报警统计
'''
def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    # 设置redis里程，传入车辆id，公共参数pdict
    setMileage.setto_redismel(vehicle_id, ex808dict, pdict['redishost'], pdict['db'], pdict['pwd'])
    datalist = readexcel()


    #从excel中获取参数
    drivertime = datalist[0][1:]
    driverspeed = datalist[1][1:]
    resttime = datalist[2][1:]
    restspeed = datalist[3][1:]

    print "驾驶时间"+str(drivertime[0])
    print "驾驶速度"+str(driverspeed[0])
    print "休息时间" + str(resttime[0])
    print "休息速度"+str(restspeed[0])
    print "上报间隔"+str(pdict['period'])


    pdict['speed']=driverspeed[0]
    tt= int(time.strftime("%H%M%S", time.localtime()))
    #初始值完后上传一次位置
    # upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
    #                          extrainfo_id, idlist, wsid, deviceid, port)

    # print sensordict
    # 控制第x次通用应答响应
    x = 0
    k = 1
    mm=0
    kk=0
    isover = False
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))
        print "开始时间"+str(t)
        if isover==True:
            print "######### 疲劳报警统计数据准备完成 #######"
            break

        while True:
            # 疲劳驾驶数据
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                print "开始发送数据"
                if kk*pdict['period'] > (int(drivertime[mm]) * 60):   #如果驾驶持续时间大于设置的持续驾驶时间，将速度设置为休息速度
                    ti = int(drivertime[mm])
                    print("-------------司机已持续驾驶%d分钟，现在是休息状态--------"%ti)
                    pdict['speed'] = restspeed[0]
                    if (kk*pdict['period'])- (int(drivertime[mm]) * 60) > (int(resttime[mm]) * 60):#如果休息时间大于设置的休息时间，将速度设置为驾驶速度
                        tii = int(resttime[mm])
                        print ("----------司机已经休息%d分钟，现在是行驶状态——————"%tii)
                        mm += 1
                        if mm == len(driverspeed):  # 如果已经遍历完了
                            isover = True
                            break
                        pdict['speed'] = driverspeed[mm]
                        kk = 0
                elif kk*pdict['period'] <= (int(drivertime[mm]) * 60):
                    print "驾驶时间未达到门限，继续行驶"


                pdict['jin'] += 0.001
                pdict['wei'] += 0.001
                ex808dict['mel'] += 0.5
                n=0

                upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                         extrainfo_id, idlist, wsid, deviceid, port)
                k += 1
                kk += 1
                print kk
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
    for i in range(16,row_num):
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


