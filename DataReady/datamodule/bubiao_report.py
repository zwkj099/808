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
    # print datalist
    getonnum =datalist[0][1]
    getoffnum =datalist[1][1]
    starttime = time.strftime("%y%m%d%H%M%S", time.localtime())  # date.strftime("%y%m%d%H%M%S")
    endtime = (datetime.datetime.now() + datetime.timedelta(seconds=600)).strftime("%y%m%d%H%M%S")

    for i in range(5):
        ##上传客流量
        # starttime = time.strftime("%y%m%d%H%M%S", time.localtime())  # date.strftime("%y%m%d%H%M%S")
        start = datetime.datetime.strptime(endtime,'%y%m%d%H%M%S')
        starttime =start .strftime("%y%m%d%H%M%S")
        starttime =(start + datetime.timedelta(seconds=30)).strftime("%y%m%d%H%M%S")
        endtime = (start + datetime.timedelta(seconds=630)).strftime("%y%m%d%H%M%S")

        footfall_data = tp.footfall_info(mobile,starttime,endtime,getonnum,getoffnum,pdict['version'])
        tp.send_data(link,footfall_data)
        getonnum += datalist[0][2]
        getoffnum +=datalist[1][2]
        time.sleep(30)

    print "###############上传客流量结束############"



# 切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa = "7e.+7e"
    re_list = re.findall(pa, str(res))
    return re_list

def readexcel():
    file_path = r'./comman/upload.xlsx'
    # file_path = r'../../comman/upload.xlsx'
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[4]
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