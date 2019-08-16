# -*- coding: utf-8 -*-
#应答脚本
import datetime
import re
import threading
import time

import testlibrary

import reply

tp=testlibrary.testlibrary()


"""
1.持续发送位置，心跳报文
2.监听接收
3.收到平台报文后，判断是否需要应答
4.需要应答时组装应答报文发送
5.应答结果配置设置
6.多线程
"""

def test1(ip,port,mobile,deviceid,vnum,name,qualification):
    print vnum
    ip=str(ip)
    port=str(port)
    mobile=str(mobile)
    deviceid=str(deviceid)
    alarm=0
    status=1
    jin =104.505043
    wei =28.173847
    high=100
    speed=80
    direction = 100
    period=30 #位置上传间隔，单位S，设定小于10时，默认10S上传
    ti=0 # 时间，0表示使用当前时间；指定时间可补传数据，格式为：190612101525
    detester = '2019-06-14 09:00:00' #补报数据开始时间，补报1小时数据，注：ti为 0时 无效
    messageid=512 #区分单条位置512和批量位置1796
    version = 0  # version=0时表示2013版808协议，version=1时表示2019版808协议

    """
    需要上传的附加信息或基于0200的扩展信息；十进制数，0或不填写表示不上传对应附加信息
    1.extrainfo_id：为808附加信息及音视频报警扩展信息
    2.idlist：外设及传感器附加信息
    3.wsid：主动安全报警附加信息
    """
    extrainfo_id = [1]  # [1,2,3,20,21,22,23,24,48,49]#传入需要组装的附件信息ID,不传表示无附加信息;1：里程，2：油量，3：速度，48：信号强度，49：卫星颗数，20：视频相关报警，21：视频信号丢失报警状态，22：视频信号遮挡报警状态，23：存储器故障报警状态，24：异常驾驶行为报警详细描述
    idlist = [83]  # [34, 39, 65,69,81,83,112,128],传入需要组装的传感器ID，十进制数；33,34,35,36,37:温度；38,39,40,41:湿度；65,66,67,68:油量、液位；69,70:油耗；81:正反转；83:里程；84:蓝牙信标；112,113:载重；128,129:工时
    wsid =[100] #上传的主动安全报警类型，（冀标只有100和101）；0: 表示不带主动安全数据；100：驾驶辅助功能报警信息；101：驾驶员行为监测功能报警信息；112：激烈驾驶报警信息；102：轮胎状态监测报警信息；103：盲区监测报警信息；113：卫星定位系统报警信息；川冀标切换只需改端口；

    # 川冀标主动安全参数
    zstatus =1#087 #主动安全车辆状态
    zalarm = deviceid #主动安全报警标识号
    sign=1 #标志状态,取值0、1、2
    event=1 #报警、事件类型，取值1、2、3、4、5、6、7、8、16、17、18
    level=1 #报警级别，取值1、2
    deviate=1#偏离类型，取值0、1、2
    road_sign=1#道路标志识别类型，取值0、1、2、3
    fatigue=1 #疲劳程度,取值0、1、2、3、4、5、6、7、8、9、10
    zds=[sign,event,level,deviate,road_sign,fatigue,jin, wei,high,speed,zstatus,zalarm]

    # 808附加信息相关参数
    vedio_alarm = 127  # 视频相关报警参数：1视频信号丢失报警，2视频信号遮挡报警，4存储单元故障报警，8其他视频设备故障报警，16客车超员报警，32异常驾驶行为报警，64特殊报警录像达到存储阈值报警,127以上全部视频相关报警
    vedio_signal = 3  # 逻辑通道号，按位计算共32位，对应位为1则对应的逻辑通道号异常，赋值时需要转换为10进制赋值
    memery = 2  # 存储器序号，按位计算，共16位，对应位为1则对应的存储器异常，bit0-bit11分别是1-12个主存储器，bit12-bit15分别是1-4个灾备存储器，赋值时需要转换为10进制赋值
    abnormal_driving = 4  # 异常驾驶行为参数：1疲劳，2打电话，4抽烟
    mel = 5000#附加信息－里程
    oil = 1#附加信息－油量
    extra_speed = 1#附加信息－行驶记录功能获取的速度
    by = 1#附加信息－信号强度
    wn = 1#附加信息－GNSS 定位卫星数
    extrainfos=[vedio_alarm, vedio_signal, memery, abnormal_driving, mel, oil, extra_speed, by, wn]

    #外设传感器相关参数
    AD=30
    Oil=20
    addoil=0
    oils=[AD,Oil,high,addoil]#油量传感器参数
    sign=1
    temp=273.1
    times=0
    warn=0
    wds = [sign,temp,times,warn]#温度传感器参数
    hum=0
    sds = [sign,hum,times,warn]#湿度传感器参数
    oilsp=0
    oiltemp=0
    tio=0
    yhs =[oilsp,oiltemp,tio,times]#油耗传感器参数
    zt=0
    fx=0
    xs=0
    li=0
    xtimes=0
    zfs =[sign,zt,fx,xs,times,li,xtimes]#正反转传感器参数
    dw=0
    zt=0
    cs=0
    zl=0
    zzzl=0
    ad1=0
    ad2=0
    ad3=0
    zzs = [sign,dw,zt,cs,zl,zzzl,ad1,ad2,ad3]#载重传感器参数
    fs=0
    ztime=0
    bd=0
    sj=0
    gss = [fs,zt,ztime,bd,sj]#工时传感器参数
    lcs = [mel,speed]#里程传感器参数

    num=1 #数据组数,本数据包含几组蓝牙信标信息数据；范围：1-6；
    UUID=111111111122222222223333333333 #蓝牙信标设备 UUID,采用 ASCII 表示
    signal=1#蓝牙信标信号强度,范围 1-100；100 最强，1 最弱；
    distance=1#终端与蓝牙信标设备的距离 单位 0.01m；范围 1-600；0xFFFF 表示没有计算距离
    battery=1 #蓝牙信标设备电池电量 百分比；范围 1-100；
    lys=[num,UUID,signal,distance,battery] #蓝牙信标数据

    link=tp.tcp_link(ip,port)
    data=tp.register(deviceid,vnum,mobile,version )
    tp.send_data(link,data)
    time.sleep(1)
    Acode=tp.receive_data(link)
    #Acode = "7E 81 00 00 13 01 99 66 66 00 01 00 02 00 01 00 37 66 62 34 64 66 39 62 62 38 64 62 34 31 32 35 08 7E" #直接使用平台返回的鉴权应答
    jqdata=tp.Authentication(Acode,mobile,version )
    tp.send_data(link,jqdata)
    time.sleep(1)
    jqres=tp.receive_data(link)
    #发送心跳数据
    heartdata = tp.heartbeat(mobile, version)
    tp.send_data(link, heartdata)
    #发送驾驶员信息
    statu=1 #0x01：从业资格证 IC 卡插入、0x02：从业资格证 IC 卡拔出（驾驶员下班）。
    result=0 #0x00：IC 卡读卡成功；0x01：读卡失败，原因为卡片密钥认证未通过；0x02：读卡失败，原因为卡片已被锁定； 0x03：读卡失败，原因为卡片被拔出； 0x04：读卡失败，原因为数据校验错误。 以下字段在 IC 卡读取结果等于 0x00 时才有效。
    institutions="重庆市渝中区大坪" #从业资格证发证机构名称
    drivers = tp.driver_information(mobile, statu, result, name, qualification, institutions)
    tp.send_data(link,drivers)
    #数据库操作
    #resul = tp.selectAll("select c.* from zw_m_config c inner join zw_m_sim_card_info s ON  s.id= c.sim_card_id  and s.simcard_number ='19966660022' and c.flag = 1")

    # base_operationdb_interface = testlibrary.opmysql.operationdb_interface()  # 实例化接口测试数据库操作类
    # resul=base_operationdb_interface.selectAll("select c.* from zw_m_config c inner join zw_m_sim_card_info s ON  s.id= c.sim_card_id  and s.simcard_number ='19966660022' and c.flag = 1")
    #print "CCC",resul
    #补传数据
    if (ti!=0):
        date = datetime.datetime.strptime(detester, "%Y-%m-%d %H:%M:%S")
        second = 30
        timelist = []
        for i in range(0, 120):#120表示1小时
            time1 = (date + datetime.timedelta(seconds=second)).strftime("%y%m%d%H%M%S")
            timelist.append(time1)
            second += 30

        for j in range(0, len(timelist)):
            extrainfos[4] += 1
            AD += 1
            Oil += 1
            high += 1
            gpsdata = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, timelist[j], direction,tp.extra_info(extrainfo_id, extrainfos), tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys), version)
            print "补传数据"
            tp.send_data(link, gpsdata)
    else:
        gpsdata = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, ti, direction, tp.extra_info(extrainfo_id,extrainfos),tp.zd_body(wsid,zds),tp.f3_attach(idlist,oils,wds,sds,yhs,zfs,zzs,gss,lcs,lys), version)
        tp.send_data(link, gpsdata)
        res = tp.receive_data(link)
        print "上线成功，维持中"
        time.sleep(1)

    #控制第x次通用应答响应
    x=0
    while True:
        #控制发送位置报文间隔
        t=int(time.strftime("%H%M%S", time.localtime()))
        while True:
            if abs(int(time.strftime("%H%M%S", time.localtime())) - t) >=period:
                extrainfos[4] += 1
                AD+=1
                Oil+=1
                high+=1
                jin+=0.001
                wei+=0.001
                gpsdata = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, ti, direction,tp.extra_info(extrainfo_id, extrainfos), tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys), version)
                tp.send_data(link,gpsdata)
                res=tp.receive_data(link)
                res=tp.dd(res)
                #切割响应
                list=ano_res(res)
                #判断响应并根据响应id回复
                # for j in list:
                #     #根据下发报文判断需要响应内容
                #     id = res[2:6]
                #     answer_number = res[22:26]
                #     reno = "01"
                #     # 平台下发指令8201，位置信息查询
                #     if id == "8201":
                #         # 组装0201位置数据，包含油量数据、里程数据
                #         mel += 1
                #         AD += 1
                #         Oil += 1
                #         high += 1
                #         oils = [AD, Oil, high,addoil]
                #         gpsbody = tp.position(mobile, 513, 2, 0, alarm, status, jin, wei, high, speed, ti, direction,mel, tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs), version,answer_number)
                #         tp.send_data(link, gpsbody)
                #
                #     # 平台下发指令8202,跟踪
                #     elif id == "8202":
                #         nu = tp.to_int(res[26:30])  # 获取回传间隔时间
                #         tim = tp.to_int(res[30:38])  # 获取跟踪有效时长
                #         print answer_number, nu, tim
                #         # 应答通用应答
                #         usual_body = reply.get_usyal_body(id, answer_number, reno)
                #         usual_head = tp.data_head(mobile, 1, usual_body, 5)
                #         usual_redata = tp.add_all(usual_head + usual_body)
                #         # tp.send_data(link, usual_redata)
                #         #reply.reply(link, res, mobile, id, answer_number, reno)
                #         i = 0
                #         while i < tim / nu:
                #             # 组装0202位置数据，包含油量数据、里程数据
                #             tp.send_data(link, usual_redata)
                #             gpsbody = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, ti,direction, mel, tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs),version, answer_number)
                #             tp.send_data(link, gpsbody)
                #             time.sleep(nu)
                #             i += 1
                #             print "第%d次发送跟踪信息：" % i
                #     else:
                #         reply.reply(link,i,mobile,id,answer_number)
                #
                t=int(time.strftime("%H%M%S", time.localtime()))
            else:
                try:
                    res=tp.receive_data(link)
                    res=tp.dd(res)
                    id = res[2:6]
                    answer_number = res[22:26]  # 应答流水号
                    #切割响应
                    #list=ano_res(res)
                    #平台下发指令8201
                    if id=="8201":
                        print answer_number
                        #组装0201位置数据，包含油量数据、里程数据
                        mel+=1
                        AD += 1
                        Oil += 1
                        high +=1
                        oils = [AD, Oil, high,addoil]
                        gpsbody = tp.position(mobile, 513, 2, 0, alarm, status, jin, wei, high, speed, ti,direction, tp.extra_info(extrainfo_id, extrainfos), tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys),version,answer_number)
                        tp.send_data(link, gpsbody)

                    # 平台下发指令8202,跟踪
                    elif id=="8202":
                        nu=tp.to_int(res[26:30]) # 获取回传间隔时间
                        tim = tp.to_int(res[30:38]) #获取跟踪有效时长
                        print answer_number,nu,tim
                        # 应答通用应答
                        #Usual(link,mobile, id, answer_number, reno)
                        # usual_body = reply.get_usyal_body(id, answer_number, reno)
                        # usual_head = tp.data_head(mobile, 1, usual_body, 5)
                        # usual_redata = tp.add_all(usual_head + usual_body)
                        # tp.send_data(link, usual_redata)
                        reply.reply(link, res, mobile, id, answer_number, reno)

                        print tim
                        i = 0
                        while i <tim/nu:
                            # 组装0200位置数据，包含油量数据、里程数
                            #gpsbody = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, ti,direction, mel, tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs,lys),version, answer_number)
                            gpsbody = tp.position(mobile, messageid, 2, 0, alarm, status, jin, wei, high, speed, ti,direction, tp.extra_info(extrainfo_id, extrainfos),tp.zd_body(wsid, zds),tp.f3_attach(idlist, oils, wds, sds, yhs, zfs, zzs, gss, lcs, lys),version, answer_number)
                            tp.send_data(link, gpsbody)
                            time.sleep(nu)
                            i += 1
                            print "第%d次发送跟踪信息："%i
                    else:
                        reply.reply(link, res, mobile, id, answer_number, reno)

                except:
                    pass
    tp.close(link)

#切割响应报文，每个响应内容一条，返回list
def ano_res(res):
    pa="7e.+7e"
    re_list=re.findall(pa,str(res))
    return re_list
#组装响应报文body
# def get_usyal_body(id,ac,reno="00"):
#     body=ac+id+reno
#     return body


#设置接入ip
ip="192.168.24.142"#"111.41.48.133"#"192.168.24.142"
#ip="zoomwell.cn"
port=6995  #6994川标,6995冀标，6975部标
deviceid=1040000
mobile=13100040000
vnum="渝B40000"
cont=0
name="艾丽11" #驾驶员姓名
qualification = 31003529463400351903 #从业资格证编码、长度 20 位，不足补 0x00。
thread_list = []
for i in range(0,1):
    t=threading.Thread(target=test1,args=(ip,port,mobile,deviceid,vnum,name,qualification))
    t.start()
    deviceid+=1
    mobile+=1
    qualification+=1
    #cont += 1
    #name = name + str(cont)
    thread_list.append(t)
    time.sleep(0.01)
for x in thread_list:
    x.join()
print ("主线程end")