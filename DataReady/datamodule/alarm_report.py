# -*- coding: utf-8 -*-
import xlrd
from comman import upload_location, reply_position,setMileage
from config import readconfig

readcig = readconfig()

"""
上传报警报表数据信息
1.设置报警标志位
2.设置传感器相关报警，上传前需要设置idlist = [传感器id...] 
"""

def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()  #每次都有testconfig中的初始值，不带上一个模块设置的值过来

    # 设置redis里程，传入车辆id，公共参数pdict
    setMileage.setto_redismel(vehicle_id, ex808dict, pdict['redishost'], pdict['db'], pdict['pwd'])

    excel_list = readexcel()
    alarmstatus =0

    for datalow in excel_list[0:29]:
        alarmstatus +=datalow[1]*(2**datalow[2])

    pdict['alarm']=alarmstatus

    if excel_list[30:31][0][1]==1:
        sensordict['warn']=excel_list[30:31][0][2]#温度
    if excel_list[31:32][0][1]==1:
        sensordict['warn'] = excel_list[31:32][0][2]#湿度
    if excel_list[32:33][0][1]==1:
        #里程超速
        sensordict['speed']=int(excel_list[32:33][0][2])
    if excel_list[33:34][0][1]==1:
        data =str(excel_list[33:34][0][2]).split('|')
        #油量,加油报警
        sensordict['addoil']=data[1]
        sensordict['Oil']=data[0]
    if excel_list[35:36][0][1]==1:
        #正反转
        sensordict['zts']=2
        sensordict['fx']=2
    if excel_list[37:38][0][1]==1:
        #载重
        sensordict['datalen']=1
    if excel_list[36:37][0][1]==1:
        #工时
        sensordict['gslen']='01'

        upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                 extrainfo_id, idlist, wsid, deviceid, port)
    print "######### 报警报表数据准备完成 #######"
    pdict['alarm']=0 #恢复不报警状态




def readexcel():
    file_path = r'./comman/upload.xlsx'
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[1]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    list = []
    for i in range(1,row_num):
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
