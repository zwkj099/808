# -*- coding: utf-8 -*-
# 应答脚本
import datetime
import re
import threading
import time

import reply
import testlibrary
from Automation.AppManager.auto_test import auto_test
from DataReady import dataready_test
from comman import buchuan1, upload_location, reply_position,attach_upload
from config import readconfig
from Applet.redis_operation import getdb_value,setMileage
from Applet.mysql_operation import  getmysql_vehicleid
import thread
tp = testlibrary.testlibrary()
readcig = readconfig()

"""
1.持续发送位置，心跳报文
2.监听接收
3.收到平台报文后，判断是否需要应答
4.需要应答时组装应答报文发送
5.应答结果配置设置
6.多线程
"""


def test1(ip, port, mobile, deviceid, vnum, name, qualification,attach,filepath,i=0,tal=0):

    ip = str(ip)
    port = str(port)
    mobile = str(mobile)
    deviceid = str(deviceid)

    #读取传感器参数
    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()

    """
    需要上传的附加信息或基于0200的扩展信息；十进制数，0或不填写表示不上传对应附加信息
    1.extrainfo_id：为808附加信息及音视频报警扩展信息
    2.idlist：外设及传感器附加信息
    3.wsid：主动安全报警附加信息
    """
    extrainfo_id = [1,2,3,20,21,22,23,24,48,49]#[1,48,49]  # [1,2,3,20,21,22,23,24,48,49]#传入需要组装的附件信息ID,不传表示无附加信息;1：里程，2：油量，3：速度，48：信号强度，49：卫星颗数，20：视频相关报警，21：视频信号丢失报警状态，22：视频信号遮挡报警状态，23：存储器故障报警状态，24：异常驾驶行为报警详细描述

   #上传wifi数据时，必须同时上传基站数据，上传基站数据，0200状态要为未定位
    idlist = [8]  # [34, 39, 65,69,79,80,81,83,112,128],传入需要组装的传感器ID，十进制数；33,34,35,36,37:温度；38,39,40,41:湿度；65,66,67,68:油量、液位；69,70:油耗；79:电量检测,80:终端检测；81:正反转；83:里程；84:蓝牙信标；112,113:载重；128,129:工时；8：基站数据；8、9：wifi数据
    wsid = [225]  # 上传的主动安全报警类型；225-231是中位主动安全数据，冀标只有100和101；0: 表示不带主动安全数据；100：驾驶辅助功能报警信息；101：驾驶员行为监测功能报警信息；112：激烈驾驶报警信息；102：轮胎状态监测报警信息；103：盲区监测报警信息；113：卫星定位系统报警信息；川冀标切换只需改端口；

    link = tp.tcp_link(ip, port)
    # 注册、鉴权、心跳
    upload_location.initial(tp, link, deviceid, vnum, mobile, pdict['version'])

    tal = int(tal)+30
    time1=''
    c = threading.RLock()
    def f():
        with c:
            date = datetime.datetime.strptime(pdict['detester'],
                                              "%Y-%m-%d %H:%M:%S")  # _strptime方法不支持多线程，运行时会报错：AttributeError: _strptime
            time1 = (date + datetime.timedelta(seconds=int(tal))).strftime("%y%m%d%H%M%S")

    # 发送驾驶员信息
    statu = 1 #0x01：从业资格证 IC 卡插入（驾驶员上班）； 0x02：从业资格证 IC 卡拔出（驾驶员下班）
    result = 0 #0x00：IC 卡读卡成功；0x01：读卡失败，原因为卡片密钥认证未通过；0x02：读卡失败，原因为卡片已被锁定； 0x03：读卡失败，原因为卡片被拔出； 0x04：读卡失败，原因为数据校验错误。
    institutions = "重庆市渝中区大坪" #发证机构名称

    ###########     需要补传驾驶员信息，最后一个参数为time1,实时上传改为0或去掉 #############################
    drivers = tp.driver_information(mobile, statu, result, name, qualification, institutions,pdict['version'],0)
    tp.send_data(link, drivers)


    #设置redis里程，传入车辆id，公共参数ex808dict
    vehicle_id = getmysql_vehicleid.get_vehicleid('192.168.24.142'  ,'root' ,'Zwkj@123Mysql' ,'clbs',vnum)
    print vehicle_id
    # setMileage.setto_redismel(vehicle_id,ex808dict,pdict['redishost'],pdict['db'],pdict['pwd'])
    # print "redis mel: "+str(ex808dict['mel'])

    #获取redis15分区namespace　GROUPINFO－>10000下的数据
    rd= getdb_value.get_15partition_keys('192.168.24.105', 15, pdict['pwd'], 'GROUPINFO:10000:53552631119085568')
    print rd
    #数据库操作    # dbop = db_operation.interface_db.interface_db()
    # print dbop.mysqldata('select * from paas_monitorInfo')

    auto = 0;  # 为0不跑自动化脚本，为１要跑自动化脚本
    aa=0
    if auto == 1:  # auto == 1，则要跑自动化脚本
        auto_test(tp, link, mobile, vnum)
    elif (pdict['ti'] != 0):  # 补传数据
        wsid1 = []
        wsid1,excel_list_k=buchuan1.deal_data(pdict, sichuandict, ex808dict, sensordict,bluetoothdict,wsid1,i)#读取excel表格数据，改变速度、初始里程、报警事件
        buchuan1.upload(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict,bluetoothdict, extrainfo_id, idlist, wsid1,excel_list_k,deviceid,port,tal)

    elif aa==1:  #数据准备，也要根据情况设置extrainfo_id,idlist ,wsid，该绑定传感器的要到平台绑定传感器
        print "数据准备开始"
        dataready_test.datatest(tp, link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id)
        print "准备数据完成"

    else:  # 正常上传位置信息
        upload_location.location(tp, link, mobile,pdict, sichuandict, ex808dict, sensordict,bluetoothdict, extrainfo_id, idlist, wsid,deviceid,port)
        res = tp.receive_data(link)
        print "上线成功，维持中"
        time.sleep(1)

    print "ok"

    # 控制第x次通用应答响应
    x = 0
    while True:
        # 控制发送位置报文间隔
        t = int(time.strftime("%H%M%S", time.localtime()))
        while True:
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >= pdict['period']:
                ex808dict['mel'] += 1
                sensordict['AD'] += 1
                sensordict['Oil'] += 1
                pdict['high'] += 1
                pdict['jin'] += 0.001
                pdict['wei'] += 0.001
                sichuandict['event'] +=1
                if(sichuandict['event']==9 ):
                    sichuandict['event'] = 16
                elif (sichuandict['event'] == 19):
                    sichuandict['event'] = 1
                    if(wsid[0]==100):
                        wsid[0]=101
                    elif (wsid[0] == 101):
                        wsid[0] = 112
                    elif(wsid[0]==112):
                        wsid[0] = 100
                    #如果是中位标准，可以先注释以上６行代码，开启下面的判断
                    # if (wsid[0] == 225):
                    #     wsid[0] = 226
                    # elif (wsid[0] == 226):
                    #     wsid[0] = 227
                    # elif (wsid[0] == 227):
                    #     wsid[0] = 228
                    # elif (wsid[0]) == 228:
                    #     wsid[0] == 225
                upload_location.location(tp, link, mobile, pdict, sichuandict, ex808dict, sensordict, bluetoothdict,
                                         extrainfo_id, idlist, wsid, deviceid, port)
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
                        # reply_position.reply_pos(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id,idlist, wsid, answer_number, res, id, reno)
                        reply_position.reply_pos(tp, link, mobile, pdict,sichuandict, ex808dict, sensordict,bluetoothdict, extrainfo_id,
                                                 idlist, wsid,  deviceid, port,answer_number, res, id, reno)

                    else:
                        reply.reply(tp,link, i, mobile, id, answer_number, reno,pdict['version'])

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
                    elif id == '9208':
                        th = threading.Thread(target=attach_upload.attach_upload, args=(tp, res, mobile, attach,filepath,pdict['version']))
                        th.start()


                    else:
                        reply.reply(tp,link, res, mobile, id, answer_number, reno,pdict['version'])

                except:
                    pass
    tp.close(link)


# 切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa = "7e.+7e"
    re_list = re.findall(pa, str(res))
    return re_list

# 设置接入ip
# ip = "192.168.24.142"  # 218.78.40.57,"111.41.48.133"#"192.168.24.142"
ip = "112.126.64.32"
port =7003  # 6994川标,6995冀标，6975部标,6996桂标，6997苏标，6998浙标，6999吉标，7000陕标,7002沪标；7003中位标准
# deviceid =9900021 #20190928
deviceid =0002555
# mobile =17799990021 #123456789
mobile =13200222555
# vnum = u"中W00021"  #桂BB001
vnum = u"渝JTS555"
cont = 0
name = "驾驶员桂A0002"
qualification = 14303529463400355011
attach = '00'  #00图片、02视频
filepath = './resourceFile/00_E1_E100_0_b87441129fb34ef8969fd0de2739d1330.jpg'

tal=0 #用于补传数据，多个监控对象时，每隔一个小时上传一个监控对象的补传数据
thread_list = []
for i in range(0, 1):
    t = threading.Thread(target=test1, args=(ip, port, mobile, deviceid, vnum, name, qualification,attach,filepath,i,tal))
    t.start()
    name = "驾驶员"
    deviceid += 1
    mobile += 1
    qualification += 1
    cont += 1
    tal += 3600
    # vnum=vnum+str(random.randint(1,100))
    name = name + str(cont)
    thread_list.append(t)
    time.sleep(0.01)
for x in thread_list:
    x.join()
print ("主线程end")