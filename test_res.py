# -*- coding: utf-8 -*-
# 应答脚本
import time
import threading
import thread
import testlibrary
import random
import re
import datetime
import reply
from config import readconfig
import db_operation
from comman import buchuan, upload_location, reply_position
from comman import Register_authentication_Heartbeat as Rah
from auto_test import auto_test

tp = testlibrary.testlibrary()
readcig = readconfig()
dbop = db_operation.db_operation()

"""
1.持续发送位置，心跳报文
2.监听接收
3.收到平台报文后，判断是否需要应答
4.需要应答时组装应答报文发送
5.应答结果配置设置
6.多线程
"""


def test1(ip, port, mobile, deviceid, vnum, name, qualification):
    #     print vnum
    ip = str(ip)
    port = str(port)
    mobile = str(mobile)
    deviceid = str(deviceid)

    pdict, sichuandict, ex808dict, sensordict, bluetoothdict = readcig.readtestfile()
    # 组装数据
    zds, extrainfos, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys = readcig.build_data(pdict, sichuandict, ex808dict,sensordict, bluetoothdict,deviceid)

    info = [zds, extrainfos, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys]

    """
    需要上传的附加信息或基于0200的扩展信息；十进制数，0或不填写表示不上传对应附加信息
    1.extrainfo_id：为808附加信息及音视频报警扩展信息
    2.idlist：外设及传感器附加信息
    3.wsid：主动安全报警附加信息
    """
    extrainfo_id = [1]  # [1,2,3,20,21,22,23,24,48,49]#传入需要组装的附件信息ID,不传表示无附加信息;1：里程，2：油量，3：速度，48：信号强度，49：卫星颗数，20：视频相关报警，21：视频信号丢失报警状态，22：视频信号遮挡报警状态，23：存储器故障报警状态，24：异常驾驶行为报警详细描述
    idlist = [65]  # [34, 39, 65,69,81,83,112,128],传入需要组装的传感器ID，十进制数；33,34,35,36,37:温度；38,39,40,41:湿度；65,66,67,68:油量、液位；69,70:油耗；81:正反转；83:里程；84:蓝牙信标；112,113:载重；128,129:工时
    wsid = [100]  # 上传的主动安全报警类型，（冀标只有100和101）；0: 表示不带主动安全数据；100：驾驶辅助功能报警信息；101：驾驶员行为监测功能报警信息；112：激烈驾驶报警信息；102：轮胎状态监测报警信息；103：盲区监测报警信息；113：卫星定位系统报警信息；川冀标切换只需改端口；

    link = tp.tcp_link(ip, port)
    # 注册、鉴权、心跳
    Rah.initial(tp, link, deviceid, vnum, mobile, pdict['version'])

    # 发送驾驶员信息
    statu = 0
    result = 0
    institutions = "重庆市渝中区大坪"
    drivers = tp.driver_information(mobile, statu, result, name, qualification, institutions)
    tp.send_data(link, drivers)

    # 数据库操作
    #     dbop.interface_db(tp,testlibrary)
    auto = 0;  # 是否要跑自动化脚本？

    if (pdict['ti'] != 0):  # 补传数据
        buchuan.upload(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id, idlist, wsid)

    elif auto == 1:  # 是否要跑自动化脚本？
        auto_test(tp, link, mobile, vnum)

    else:  # 正常上传位置信息
        upload_location.location(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id, idlist, wsid)
        res = tp.receive_data(link)
        print "上线成功，维持中"
        time.sleep(1)

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
                info = readcig.build_data(pdict, sichuandict, ex808dict, sensordict, bluetoothdict, deviceid)
                upload_location.location(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id, idlist,wsid)
                res = tp.receive_data(link)
                res = tp.dd(res)
                # 切割响应
                list = ano_res(res)
                # 判断响应并根据响应id回复
                for j in list:
                    # 根据下发报文判断需要响应内容
                    id = res[2:6]
                    answer_number = res[22:26]
                    reno = "01"

                    if id in ["8201", "8202"]:
                        reply_position.reply_pos(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id,idlist, wsid, answer_number, res, id, reno)

                    else:
                        reply.reply(link, i, mobile, id, answer_number)

                t = int(time.strftime("%H%M%S", time.localtime()))
            else:
                try:
                    reno = "01"
                    res = tp.receive_data(link)
                    res = tp.dd(res)
                    id = res[2:6]
                    answer_number = res[22:26]  # 应答流水号
                    # 切割响应
                    # list=ano_res(res)
                    if id in ["8201", "8202"]:
                        try:
                            reply_position.reply_pos(tp, link, mobile, pdict, ex808dict, sensordict, info, extrainfo_id,idlist, wsid, answer_number, res, id, reno)
                        except Exception as e:
                            print e
                    else:
                        reply.reply(link, res, mobile, id, answer_number, reno)

                except:
                    pass
    tp.close(link)


# 切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa = "7e.+7e"
    re_list = re.findall(pa, str(res))
    return re_list

# 设置接入ip
ip = "192.168.24.142"  # "111.41.48.133"#"192.168.24.142"
# ip="zoomwell.cn"
port = 6995  # 6994川标,6995冀标，6975部标
deviceid = 1040000
mobile = 13100040000
vnum = u"渝B40000"
cont = 0
name = "艾丽11"
qualification = 14003529463400352903
thread_list = []
for i in range(0, 1):
    t = threading.Thread(target=test1, args=(ip, port, mobile, deviceid, vnum, name, qualification))
    t.start()
    deviceid += 1
    mobile += 1
    qualification += 1
    cont += 1
    # vnum=vnum+str(random.randint(1,100))
    name = name + str(cont)
    thread_list.append(t)
    time.sleep(0.01)
for x in thread_list:
    x.join()
print ("主线程end")