# -*- coding: utf-8 -*-
import xlrd
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
0x14;设置视频报警标志位，设置需要要上传哪种报警
0x15:视频信号丢失报警状态逻辑通道号设置，对应位为1表示视频信号丢失  vedio_signal
0x16:视频信号遮挡报警状态逻辑通道号设置，对应位为1表示视频信号遮挡 vedio_signal
0x17:存储器故障故障报警状态   memery
0x18:异常驾驶行为报警详细描述：1疲劳，2打电话，4抽烟  abnormal_driving

extrainfo_id = [20,21,22,23,24] 
"""

def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    # 设置redis里程，传入车辆id，公共参数pdict
    setMileage.setto_redismel(vehicle_id, ex808dict, pdict['redishost'], pdict['db'], pdict['pwd'])
    excel_list = readexcel()
    alarmstatus =0

    for datalow in excel_list[0:7]:
        alarmstatus +=datalow[1]*(2**datalow[2])

    # print "vedio_alarm:"+str(alarmstatus)

    ex808dict['vedio_alarm']=alarmstatus  #给视频相关报警的变量赋值
    ex808dict['vedio_signal']=3
    ex808dict['memery']=2
    ex808dict['abnormal_driving']=4

    upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                             extrainfo_id, idlist, wsid, deviceid, port)
    print "######### 普货报表数据准备完成 #######"
    pdict['vedio_alarm']=0 #恢复不报警状态


    # # print sensordict
    # # 控制第x次通用应答响应
    # x = 0
    # k = 1
    # while True:
    #     # 控制发送位置报文间隔
    #     t = int(time.strftime("%H%M%S", time.localtime()))
    #     if k>5:
    #         print "######### 普货报表数据准备完成 #######"
    #         break
    #
    #     while True:
    #         if k>5:
    #             pdict['vedio_alarm'] = 0  # 恢复不报警状态
    #             break
    #
    #         if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
    #             pdict['jin'] += 0.001
    #             pdict['wei'] += 0.001
    #
    #             upload_location.location(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id, idlist,wsid)
    #             k += 1
    #             res = tp.receive_data(link)
    #             res = tp.dd(res)
    #             # 切割响应
    #             list = ano_res(res)
    #             # 判断响应并根据响应id回复
    #             for j in list:
    #                 # 根据下发报文判断需要响应内容
    #                 id = res[2:6]
    #                 # 应答流水号
    #                 if pdict['version']==0:
    #                     answer_number = res[22:26]
    #                 elif pdict['version']==1:
    #                     answer_number = res[32:36]
    #                 reno = "00"
    #                 if id in ["8201", "8202","8802","8500"]:
    #                     reply_position.reply_pos(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id,idlist, wsid, answer_number, res, id, reno)
    #
    #                 else:
    #                     reply.reply(tp,link, res, mobile, id, answer_number, reno,pdict['version'])
    #
    #             t = int(time.strftime("%H%M%S", time.localtime()))
    #         else:
    #             try:
    #                 reno = "00"
    #                 res = tp.receive_data(link)
    #                 res = tp.dd(res)
    #                 id = res[2:6]
    #                 # 应答流水号
    #                 if pdict['version']==0:
    #                     answer_number = res[22:26]
    #                 elif pdict['version']==1:
    #                     answer_number = res[32:36]
    #                 # 切割响应
    #                 #list=ano_res(res)
    #                 if id in ["8201", "8202","8802","8500"]:
    #                     try:
    #                         reply_position.reply_pos(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id,idlist, wsid, answer_number, res, id, reno)
    #                     except Exception as e:
    #                         print e
    #                 else:
    #                     reply.reply(tp,link, res, mobile, id, answer_number, reno,pdict['version'])
    #
    #             except:
    #                 pass

# 切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa = "7e.+7e"
    re_list = re.findall(pa, str(res))
    return re_list


def readexcel():
    file_path = r'./comman/upload.xlsx'
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[7]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    list = []
    for i in range(2,row_num):
        rowlist = []
        if data_sheet.cell_value(i, 1) != '':
            for j in range(col_num):

                    if isinstance(data_sheet.cell_value(i, j),float):
                        rowlist.append(int(data_sheet.cell_value(i, j)))
                    else:
                        rowlist.append(data_sheet.cell_value(i, j))
        if rowlist!=[]:
            list.append(rowlist)
    return  list

# excel_list = readexcel()
# print excel_list[0:29]
