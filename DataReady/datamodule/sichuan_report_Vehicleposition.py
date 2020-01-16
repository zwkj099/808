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
   四川监管报表：车辆定位统计
   （1）车辆管理中设置车辆不能为客车
   （2）在报警设置平台报警中设四川标准的超速报警
   下面上传的是持续超速报警

"""
def main(args,testinfo,tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    # 设置redis里程，传入车辆id，公共参数pdict
    setMileage.setto_redismel(vehicle_id, ex808dict, pdict['redishost'], pdict['db'], pdict['pwd'])
    datalist=[]
    datalist = readexcel()
    print "datalist start:\n"
    print datalist

    statuslist = datalist[0][1:]
    jinlist = datalist[1][1:]
    weilist = datalist[2][1:]
    wnlist = datalist[3][1:]
    interrupt_num = datalist[4][1:]
    interrupt_drift = datalist[5][1:]
    lasttime = datalist[6][1:]

    jin = pdict['jin']
    wei= pdict['wei']

    pdict['status'] = statuslist[0]
    pdict['jin'] = jin if jinlist[0] == 1 else jinlist[0]
    pdict['wei'] = wei if weilist[0] == 1 else weilist[0]
    ex808dict['wn'] = wnlist[0]
    # ex808dict['mel']=177

    print "######### 车辆定位统计数据准备开始 #######"
    #初始值完后上传一次位置
    upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                             extrainfo_id, idlist, wsid, deviceid, port)

    # 控制第x次通用应答响应
    x = 0
    mm=0
    kk=0
    isover = False
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))
        if isover==True:
            print "######### 车辆定位统计数据准备完成 #######"
            break

        while True:
            tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1),
                                                 hour=0, minute=0, second=0)
            if (tomorrow - datetime.datetime.now()).seconds==0: #如果到每天零点，里程设为100
                ex808dict['mel']=100
            # ##持续超速统计
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                if interrupt_num[mm]!=0:
                    pdict['status']=1
                    if interrupt_drift[mm]!=0:###如果有中断,经纬度变化大点以便离线位移时位移大于50km
                        pdict['jin'] += 0.2
                        pdict['wei'] += 0.2
                        if kk*pdict['period']%(30*60)==0:
                            pdict['status']=3 #变成定位
                    elif interrupt_drift[mm]==0 and kk*pdict['period']%(10*60)==0:
                        pdict['status'] = 3  # 变成定位
                    else:
                        pdict['status']=1

                # if kk*pdict['period']==(int(lasttime[mm]) * 60+pdict['period']):
                #     pdict['speed'] = setspeed - 10
                if kk*pdict['period']==(int(lasttime[mm]) * 60+pdict['period']):
                    mm += 1
                    if pdict['jin']!=0 and pdict['wei']!=0:
                        jin = pdict['jin']  #如果遍历完一种上传，下一种的经纬度从此经纬度开始
                        wei = pdict['wei']
                    if mm == len(statuslist):#如果已经遍历完了
                        print "上传数据结束了..."
                        isover = True

                        break
                    print "######### 下一个阶段数据开始 #######"
                    pdict['status'] =statuslist[mm]
                    pdict['jin']=jin if jinlist[mm]==1 else float(jinlist[mm])
                    pdict['wei']=wei if weilist[mm]==1 else float(weilist[mm])
                    ex808dict['wn']=wnlist[mm]
                    kk = 0

                if pdict['jin']!=0 and pdict['wei']!=0:
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
    for i in range(8,row_num):
        rowlist = []
        if data_sheet.cell_value(i, 1) != '':
            for j in range(col_num):
            # for j in range(6, col_num):#从第几列开始运行数据，就写多少列
                valuex=data_sheet.cell_value(i, j)
                if valuex!='':
                    if re.findall(r'^\d+\.0$', str(valuex), re.I) != []:
                        rowlist.append(int(valuex))

                    else:
                        rowlist.append(valuex)

        if rowlist!=[]:
            list.append(rowlist)

    return  list

# list = readexcel()
# print list