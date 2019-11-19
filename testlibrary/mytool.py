#!/usr/bin/env Python
# -*- coding: utf-8 -*-
# v2.0：重新规划各种方法，基础校验封装写到jctool.py，部分非常规写到expe.py，本文件只写基础组装报文、解析、socket方法，逻辑将全部外放处理
#本测试库，把消息按照消息头，消息体，附加消息，f3附加消息进行组装，具体可依据协议
#也可支持应答

import random, time, struct, binascii
import socket
import sys
import math
import json, xml
import requests, urllib
import re
import datetime
from jctool import jctool

jctool = jctool()

reload(sys)
sys.setdefaultencoding('utf8')


class mytool(object):
    def __init__(self):
        pass

    # 组装head头，传入参数包括手机号，消息id，消息体，流水号（可不传，默认0000）
    def data_head(self, mobile, newid, data, xulie=1,version=0):
        '''
        组装消息头
        :param mobile: 手机号
        :param newid:消息id，如0100,0200
        :param data:消息体，包括基本信息，附加信息，f3信息
        :param xulie:消息流水号，默认0000
        :param version:协议版本，１表示808-2019，０表示808-2013
        :return:对应消息id的消息头信息
        '''
        lenth = len(data) / 2
        if version==0:
            while len(mobile) < 12:
                mobile = "0" + mobile
            head = jctool.to_hex(newid,4) + jctool.to_hex(lenth, 4) + str(mobile) + jctool.to_hex(xulie, 4)
        elif version==1:
            while len(mobile) < 20:
                mobile = "0" + mobile
            head = jctool.to_hex(newid, 4) + jctool.to_hex(64, 2) + jctool.to_hex(lenth, 2) + jctool.to_hex(version,2) + str(mobile) + jctool.to_hex(xulie, 4)
        return head
    # 组装报文body，传入ascii码的设备号和车牌号
    def data_zc_body(self, deviceid, vnum,version):
        '''
        组装注册报文body
        :param deviceid: 设备号，7位数字字母
        :param vnum: 标准7位车牌号
        :param version:协议版本，１表示808-2019，０表示808-2013
        :return: 注册报文body
        '''
        if version==0:
            body = jctool.to_hex(13, 4) + jctool.to_hex(1100, 4) + jctool.to_hex(0, 10) + jctool.to_hex(0,40) + jctool.get_id(deviceid) + jctool.to_hex(2, 2) + jctool.get_vnum(vnum)
        else:
            while len(deviceid) < 30:
                deviceid = "0" + deviceid
            body = jctool.to_hex(13, 4) + jctool.to_hex(1100, 4) + jctool.to_hex(0, 22) + jctool.to_hex(0,60) + jctool.get_id(deviceid) + jctool.to_hex(2, 2) + jctool.get_vnum(vnum)
        return body
    # 组装报文body，传入ascii码的设备号和车牌号

    # 获取鉴权码
    def data_jq_body(self, zcres,version):
        '''
        从注册响应获取鉴权码，即鉴权报文body
        :param zcres: 注册时的响应,响应报文需处理为末端不带空格
        :param version:协议版本，１表示808-2019，０表示808-2013
        :return: 鉴权报文body，即鉴权码
        '''
        if version==1:
            a = str(zcres)
            a = jctool.dd(a)
            a = a[40:-4]
            body = jctool.to_hex(len(a) / 2, 2) + a + jctool.to_hex(0, 30) + jctool.to_hex(0, 40)
        else:
            a = str(zcres)
            a = jctool.dd(a)
            a = a[32:-4]
            body=a
        return body

    def Position_New(self,messageid ,number=0,type=0,alarm=0, status=0, jin=0, wei=0, high=0, speed=0, ti=0, direction=0,f3body=-1,answer_number=0000 ):
        '''
       组装位置信息，通过messageid判断是发单条位置还是发批量位置信息
        :param messageid :消息ID
        :param number:数据项个数，批量位置信息时有效（1796）
        :param type:位置数据类型，批量位置信息时有效（1796）
        :param alarm: 报警标志位，传入0默认无报警,十进制数
        :param status: 状态位，传入0默认定位，acc开，十进制数
        :param jin:经度
        :param wei: 纬度
        :param high:高度
        :param speed:速度
        :param ti:时间，0默认当前时间
        :param direction:方向
        :param meliage:里程，值为-1时表示不组装里程数据
        :param answer_number:应答流水号，ID为513时有效
        :return:位置报文基本信息
        '''
        #转化单位和格式
        jin = float(jin) * 1000000
        wei = float(wei) * 1000000
        speed = float(speed) * 10
        if f3body==-1:
            f3body=""
        data0=jctool.to_hex(alarm, 8) + jctool.to_hex(status, 8) + jctool.to_hex(wei, 8) + jctool.to_hex(jin,8) + jctool.to_hex(high, 4) + jctool.to_hex(speed, 4) +jctool.to_hex(direction, 4)
        # ti如果传入0,表示取当前系统时间
        if int(ti) == 0:
            ti = time.strftime("%y%m%d%H%M%S", time.localtime())

        if messageid in (512,2050,1796):
            body = data0+ str(ti) + f3body #+ meliage + f3body
            return body
        elif  messageid in (513,1280):
            body =answer_number + data0+ str(ti) + f3body
            return body
        else:
            print "消息ID有误，请输入位置消息ID 512或1796"

    def zd_body(self,ids=None, zds=None,ti=0):
        '''组装主动安全附加信息
        :param ids: 外设ID,可以同时传入多个（100、101、102、103、112、113）
        :param sign:标志状态
        :param event:报警、事件类型
        :param level:报警级别
        :param deviate:偏离类型
        :param road_sign:道路标志识别类型
        :param fatigue:疲劳程度
        :param jin:经度
        :param  wei:纬度
        :param high:高程
        :param speed:速度
        :param zstatus:状态
        :param zalarm:报警
        :param returnr:返回主动安全报警数据
        '''
        ZDAQ_body = ""
        sign, event, level, deviate, road_sign, fatigue,jin, wei, high, speed, zstatus, deviceid,attach_Count=zds
        for id in ids:
            if id in (100,101,102,103,112,113):
                body = self.add_zdaq(id, sign, event, level, deviate, road_sign, fatigue, jin, wei, high, speed, zstatus,deviceid,attach_Count)
                ZDAQ_body += body
            else:
                print "无主动安全数据"
        return ZDAQ_body

    def f3_attach(self,ids=None, oils=None, wds=None, sds=None, yhs=None, zfs=None, zzs=None, gss=None, lcs=None,lys=None):
        '''组装F3附加信息，目前只实现了油量
                    :param ids: 传感器ID，十进制数
                    :param Oils:油量相关参数，包含 AD值,oil加油量,high液位高度
                    :param wds: 温度相关参数
                    :param sds: 湿度相关参数
                    :param yhs: 油耗相关参数
                    :param zfs: 正反转相关参数
                    :param zzs: 载重相关参数
                    :param gss: 工时相关参数
                    :param lcs: 里程相关参数
                    :param return:返回F3附加信息
                    '''
        data = ""
        cont = 0
        for i in ids:
            if i in (33,34,35,36,37):# 温度
                sign, temp, times, warn = wds
                data += self.add_wd(i, sign, temp, times, warn)
                cont = cont + 1
            elif i in (38,39,40,41):# 湿度
                sign, hum, times, warn = sds
                data += self.add_sd(i, sign, hum, times, warn)
                cont = cont + 1
            elif i in (65,66,67,68):# 油量、液位
                AD, Oil, high,addoil= oils
                data += self.add_yw(i, 0, AD, 300, 310, addoil, 0, Oil, 0, high)
                cont = cont + 1
            elif i in (69,70):# 油耗
                oilsp, oiltemp, tio, times = yhs
                data += self.add_yh(i, oilsp, oiltemp, tio, times)
                cont = cont + 1
            elif i == 81:  # 正反转
                sign, zt, fx, xs, times, li, xtimes = zfs
                data += self.add_zf(i, sign, zt, fx, xs, times, li, xtimes)
                cont = cont + 1
            elif i == 83:  # 里程
                lc, sp = lcs
                data += self.add_lc(i, lc, sp)
                cont = cont + 1
            elif i == 84:  # 蓝牙信标
                num, UUID, signal, distance, battery = lys
                data += self.add_ly(i, num,UUID,signal,distance,battery)
                cont=cont+1
            elif i in (112,113):#载重
                sign, dw, zt, cs, zl, zzzl, ad1, ad2, ad3 = zzs
                data += self.add_zz(i, sign, dw, zt, cs, zl, zzzl, ad1, ad2, ad3)
                cont = cont + 1
            elif i in (128,129):# 工时
                fs, zt, ztime, bd, sj = gss
                data += self.add_gs(i, fs, zt, ztime, bd, sj)
                cont = cont + 1
        return self.add_f3_data(cont, data)

    def add_zdaq(self,id,sign,event,level,deviate,road_sign,fatigue,jin, wei, high, speed,zstatus,deviceid,attach_Count):
        ''' 川冀标主动安全数据
        :param id: 外设ID（100、101、102、103、112、113）
        :param sign:标志状态
        :param event:报警、事件类型
        :param level:报警级别
        :param deviate:偏离类型
        :param road_sign:道路标志识别类型
        :param fatigue:疲劳程度
        :param jin:经度
        :param  wei:纬度
        :param high:高程
        :param speed:速度
        :param zstatus:状态
        :param deviceid:报警中的终端ＩＤ字段
        :param attach_Count:报警中的附件数量
        '''
        jin = float(jin) * 1000000
        wei = float(wei) * 1000000
        ti = time.strftime("%y%m%d%H%M%S", time.localtime())
        # date = datetime.datetime.strptime('2019-08-08 09:00:00', "%Y-%m-%d %H:%M:%S")
        # ti = date.strftime("%y%m%d%H%M%S")
        alarm= jctool.get_id(deviceid)+str(ti)+"00"+jctool.to_hex(attach_Count, 2)+"00"
        data0=jctool.to_hex(speed, 2) + jctool.to_hex(high, 4) + jctool.to_hex(wei, 8) + jctool.to_hex(jin, 8) + str(ti) + jctool.to_hex(zstatus,4) + alarm
        # 驾驶辅助功能报警信息
        if id==100:
            data = "00000001"+jctool.to_hex(sign, 2)+jctool.to_hex(event, 2)+ jctool.to_hex(level, 2) + jctool.to_hex(speed, 2) + "09"+jctool.to_hex(deviate, 2) + jctool.to_hex(road_sign, 2)+"00" + data0
        # 驾驶员行为监测功能报警信息
        elif id==101:
            data = "00000001"+jctool.to_hex(sign, 2)+jctool.to_hex(event, 2)+ jctool.to_hex(level, 2)+jctool.to_hex(fatigue, 2) + "00000000" + data0
        # 激烈驾驶报警信息
        elif id==112:
            data = "00000001"+jctool.to_hex(sign, 2)+jctool.to_hex(event, 2)+ "0009" + "0008" + "0008"+ data0
        # 轮胎状态监测报警信息
        elif id==102:
            data = "0000000100" + data0 + "00"

        # 盲区监测报警信息
        elif id==103:
            data = "000000010001" + data0
        # 卫星定位系统报警信息
        elif id==113:
            data = "000000010001000900" + data0
        else:
            print "无主动安全数据",id
            data=""
        lent = len(data) / 2 + 1
        # 组装为cb信息并返回
        cbdata = jctool.to_hex(id, 2) + jctool.to_hex(lent, 2) + data
        return cbdata

    def extra_info(self, ids=None, extrainfos=None): #vedio_alarm=0, vedio_signal=0, memery=0, abnormal_driving=0, meilage=0, oil=0,speed=0, by=0, wn=None):
        """# 组装附加信息"""
        vedio_alarm, vedio_signal, memery, abnormal_driving, meilage, oil, extra_speed, by, wn,temper=extrainfos
        data = ""
        for i in ids:
            if i == 1:
                meilage = int(float(meilage) * 10)  #里程，DWORD，1/10km，对应车上里程表读数
                data += self.add_additional(i, 4, meilage)
            elif i == 2:
                oil = int(float(oil) * 10) #油量，WORD，1/10L，对应车上油量表读数
                data += self.add_additional(i, 2, oil)
            elif i == 3:
                speed = int(float(extra_speed) * 10)#行驶记录功能获取的速度，WORD，1/10km/h
                data += self.add_additional(i, 2, speed)
            elif i == 6:
                data +=self.add_additional(i,2,temper) #车箱温度
            elif i == 20:
                data += self.add_additional(i, 4, vedio_alarm)# 1078协议，视频相关报警
            elif i in (21, 22):
                data += self.add_additional(i, 4, vedio_signal)  # 1078协议，视频信号丢失报警状态、视频信号遮挡报警状态
            elif i == 23:
                data += self.add_additional(i, 2, memery)# 1078协议，存储器故障报警状态
            elif i == 24:
                data += self.add_additional(i, 2, abnormal_driving)#1078协议，异常驾驶行为报警详细描述
            elif i == 48:
                data += self.add_additional(i, 1, by)#无线通信网络信号强度
            elif i == 49:
                data += self.add_additional(i, 1, wn)#GNSS 定位卫星数
            else:
                print "无附加信息", i
                data = ""
        return data

    def position(self,mobile,messageid, number, type,alarm, status, jin, wei, high, speed, ti, direction,extra_info,zd_body,F3data,version=0,answer_number=0000):
        """组装位置信息0200或0704或0201
        :param mobile:手机号
        :param messageid:消息ID
        :param number: 数据项个数，批量位置信息时有效（1796）
        :param type:位置数据类型，批量位置信息时有效（1796）
        :param zd_body: 主动安全信息
        :param F3data:F3信息
        :param version:协议版本，１表示808-2019，０表示808-2013
        :param answer_number:应答流水号
        :return:返回组装后的位置信息
        """
        attach=str(extra_info)+zd_body+F3data
        if messageid == 2050:
            """应答流水+多媒体数据总项数+检索项{多媒体ＩＤ(dword)+多媒体类型(b)+通道ＩＤ(b)+事件项编码(b)+位置}"""
            gpsbody = answer_number + "0001" + "00000001" + "020707" + self.Position_New(messageid, number, type, alarm, status, jin, wei, high, speed, ti, direction,-1, answer_number)
        elif messageid == 1796:
            body=""
            NO=number
            if ti!=0:
                detester = "2019-08-15 09:00:00"
                date = datetime.datetime.strptime(detester, "%Y-%m-%d %H:%M:%S")
                second = 30
                timelist = []
                for i in range(0, NO):  # 120表示1小时
                    time1 = (date + datetime.timedelta(seconds=second)).strftime("%y%m%d%H%M%S")
                    timelist.append(time1)
                    second += 30
                for j in range(0, NO):
                    gpsbody = self.Position_New(messageid, number, type, alarm, status, jin, wei, high, speed, timelist[j],direction, attach, answer_number)
                    lenth = len(gpsbody) / 2
                    data = jctool.to_hex(lenth, 4) + gpsbody
                    NO -= 1
                    body = data + body
                    if NO==0:
                        gpsbody = jctool.to_hex(number, 4) + jctool.to_hex(type, 2) + body
                        break
            elif ti==0:
                while NO!=0:
                    gpsbody = self.Position_New(messageid, number, type, alarm, status, jin, wei, high, speed, ti, direction,attach, answer_number)
                    lenth = len(gpsbody) / 2
                    data = jctool.to_hex(lenth, 4) + gpsbody
                    NO -=1
                    body=data+body
                    time.sleep(2)
                gpsbody=jctool.to_hex(number, 4) + jctool.to_hex(type, 2) + body
        else:
            gpsbody = self.Position_New(messageid, number, type, alarm, status, jin, wei, high, speed, ti, direction,attach, answer_number)
        return gpsbody

    def heartbeat(self, mobile,version=0):
        """组装心跳信息
        :param version:协议版本，１表示808-2019，０表示808-2013
        """
        hbody = []
        hhead = self.data_head(mobile,  2, hbody, 1, version)
        data = self.add_all(hhead)
        return data

    def driver_information(self,mobile,statu,result,name,qualification,institutions,version=0,ti=0):
        """组装驾驶员信息采集上报0702
        :param mobile:手机号
        :param statu:状态
        :param result: IC 卡读取结果
        :param name:驾驶员姓名
        :param qualification: 从业资格证编码
        :param institutions:发证机构名称
        :param version:协议版本，１表示808-2019，０表示808-2013
        :return:返回组装后的驾驶员信息
        """
        if ti==0:
            ti = time.strftime("%y%m%d%H%M%S", time.localtime()) #插卡/拔卡时间
        else:
            ti=ti
        dnlength=len(jctool.character_string(name))/2 #驾驶员姓名长度
        znlength =len(jctool.character_string(institutions))/2 #发证机构名称长度
        dbody0 = jctool.to_hex(statu, 2) + str(ti)#拔卡上传信息
        dbody = dbody0 + jctool.to_hex(result, 2) + jctool.to_hex(dnlength,2) + jctool.character_string(name) + jctool.character_string(qualification, 20) + jctool.to_hex(znlength,2) + jctool.character_string(institutions) + "20200908"#插卡上传信息
        if statu == 2:
            dbody = dbody0
        elif statu == 1 and version==1 :
            dbody = dbody + jctool.character_string(qualification, 20)
        hhead = self.data_head(mobile, 1794, dbody, 1,version)
        data = self.add_all(hhead+dbody)
        return data

    def cat_data(self,data):
        # 分割收到的报文（多条），返回list
        list=re.findall(r'7E .+? 7E',data)
        return list

    def data_tc_body(self,num,data):
        # 组装obd透传0900body
        body="FA"+jctool.to_hex(num,2)+"A0"+data
        return body

    def ans(self,a1,a2,mobile,hid,reno="00"):
        '''
        :param a1:应答id
        :param a2: 应答的那条下发信息的流水号
        :param mobile:
        :param reno: 应答结果，默认成功
        :return:
        '''
        resbody=str(a2)+str(a1)+str(reno)
        reshead=self.data_head(str(mobile),str(hid),resbody,"0002")
        data=jctool.add_all(reshead+resbody)
        return str(data)

    def add_additional(self, id, size,information):
        '''
            组装附加信息
            :param id: 附加信息ＩＤ
            :param size: 附加信息长度
            :param information: 附加信息
            :return: 组装的附加信息
                           '''
        data = jctool.to_hex(id, 2) + jctool.to_hex(size, 2) + jctool.to_hex(information, size*2)
        return data

    def add_f3_data(self,num,data_body):
        '''组装传感器信息组合f3信息，把各个传感器信息打包成f3附加信息
        :param num:传感器数量
        :param data_body: 传感器信息body
        :return: f3附加信息
        '''
        f3data=""
        if num!=0:
            lent=len(data_body)/2+1 #计算f3附加消息长度
            f3data="F3"+jctool.to_hex(lent,2)+jctool.to_hex(num,2)+data_body #组装为f3信息
        return f3data

    def add_cb_data(self,id,data_body):
        '''组装四川标准主动安全信息
        组合附加信息，把各个传感器信息打包成f3附加信息
        :param id:外设ID
        :param data_body: 外设信息body
        :return: 附加信息
        '''
        #计算附加消息长度
        lent=len(data_body)/2+1
        #组装为cb信息并返回
        cbdata=jctool.to_hex(id,2)+jctool.to_hex(lent,2)+data_body
        return cbdata

    def add_jz(self,dm,dbm):
        '''基站定位
        :param dm: 定位模式，0-4
        :param dbm: 信号强度，dbm
        :return:
        '''
        data="08240000000000"+jctool.to_hex(dm,2)+"01014543010101CC05500000589000260022"+\
             jctool.to_hex(dbm,2)+"00C003A405080000000000"
        return data

    def add_wd(self,id,sign,temp,times,warn=0):
        '''温度传感器报文
        :param id: 温度传感器id（21-25对应33-37）
        :param sign: 重要数据标识（0-普通，1-重要）
        :param temp:温度值，0.1K
        :param times:状态持续时间，s
        :param warn:高低温告警（1-高温，2-低温，其他-无）
        :return:温度传感器报文
        '''
        if int(warn)==1:
            wa="00010000"
        elif int(warn)==2:
            wa="00000001"
        else:
            wa="00000000"
        temp=float(temp)*10
        data=jctool.to_hex(id,2)+"0C"+jctool.to_hex(sign,2)+jctool.to_hex(temp,6)+jctool.to_hex(times,8)+wa
        return data

    def add_sd(self,id,sign,hum,times,warn=0):
        '''
        湿度传感器报文
        :param id: 湿度传感器id（26-2a对应38-42）
        :param sign:重要数据标识（0-普通，1-重要）
        :param hum:湿度，0.1%
        :param times:超出阀值持续时间，s
        :param warn:湿度报警（1上限，2下限，其他-无）
        :return:湿度传感器报文
        '''
        if int(warn)==1:
            wa="00010000"
        elif int(warn)==2:
            wa="00000001"
        else:
            wa="00000000"
        hum=float(hum)*10
        data=jctool.to_hex(id,2)+"0C"+jctool.to_hex(sign,2)+jctool.to_hex(hum,6)+jctool.to_hex(times,8)+wa
        return data

    def add_yw(self,id,sign,high_AD,temp1,temp2,add,seep,all,ratio,high):
        '''
        组装液位传感器数据
        :param id: 液位传感器id（41-44,47-4e,对应65-68,71到78）
        :param sign:（0-普通，1-重要）
        :param high_AD:液位高度ad值
        :param temp1:液温，0.1K
        :param temp2:环温，0.1K
        :param add:加油量，0.1L
        :param seep:漏油量，0.1L
        :param all:液量，0.1L
        :param ratio:液位百分比，0.1%
        :param high:液位高度，0.1mm
        :return:液位传感器报文
        '''
        temp1=float(temp1)*10
        temp2=float(temp2)*10
        add=float(add)*10
        seep=float(seep)*10
        all=float(all)*10
        ratio=float(ratio)*1000
        data=jctool.to_hex(id,2)+"20"+jctool.to_hex(sign,2)+jctool.to_hex(high_AD,6)+jctool.to_hex(temp1,8)+\
             jctool.to_hex(temp2,8)+jctool.to_hex(add,8)+jctool.to_hex(seep,8)+jctool.to_hex(all,8)+\
            jctool.to_hex(ratio,8)+jctool.to_hex(high,8)
        return data

    def add_yh(self,id,oilsp,oiltemp,tio,times):
        '''
        获取油耗传感器报文
        :param id: 油耗传感器id（45,46,对应69,70）
        :param oilsp:累计油耗，0.01L
        :param oiltemp:油箱温度，0.1K
        :param tio:瞬时油耗，0.01L
        :param times:累计时间，0.1H
        :return:油耗传感器报文
        '''
        oilsp=float(oilsp)*100
        oiltemp=float(oiltemp)*10
        tio=float(tio)*100
        times=float(times)*10
        data=jctool.to_hex(id,2)+"10"+jctool.to_hex(oilsp,8)+jctool.to_hex(oiltemp,8)+jctool.to_hex(tio,8)+\
            jctool.to_hex(times,8)
        return data

    def add_zf(self,id,sign,zt,fx,xs,times,li,xtimes):
        '''
        组装正反转传感器报文
        :param sign:重要数据标识（0-正常，2-重要）
        :param zt:旋转状态（1-停止，2-运转）
        :param fx:旋转方向（1-顺，2-逆）
        :param xs:旋转速度r/min
        :param times:累计运行时间，0.1h
        :param li:累计脉冲数量
        :param xtimes:旋转方向持续时间，1min
        :return:正反转传感器报文
        '''
        times=float(times)*10
        data=jctool.to_hex(id,2)+"18"+jctool.to_hex(sign,2)+jctool.to_hex(zt,6)+jctool.to_hex(fx,8)+jctool.to_hex(xs,8)+jctool.to_hex(times,8)+jctool.to_hex(li,8)+jctool.to_hex(xtimes,8)
        return data

    def add_ly(self,id,count,UUID,signal,distance,battery):
        '''
        组装蓝牙数据
        :param id:外设ＩＤ
        :param count:数据组数
        :param UUID:蓝牙信标设备 UUID
        :param signal:蓝牙信标信号强度
        :param　distance:终端与蓝牙信标设备的距离
        :param　Battery:蓝牙信标设备电池电量
        :return:蓝牙报文
        '''
        data0=jctool.get_id(UUID)+jctool.to_hex(signal,2)+jctool.to_hex(distance,4)+jctool.to_hex(battery,2) #jctool.to_hex(UUID,64)
        data=data0
        while count >1:
            count=count-1
            data=data+data0
        size=len(data)/2 + 1
        data=jctool.to_hex(id,2)+jctool.to_hex(size,2)+jctool.to_hex(count,2)+data
        return data

    def add_lc(self, id, lc, sp):
        '''
        组装里程传感器数据
        :param lc:累计里程，0.1KM
        :param sp:车速，km/h
        :return:里程传感器报文
        '''
        lc = float(lc) * 10
        data = jctool.to_hex(id, 2) + "08" + jctool.to_hex(lc, 8) + jctool.to_hex(sp, 8)
        return data

    def add_zz(self,id,sign,dw,zt,cs,zl,zzzl,ad1,ad2,ad3):
        '''
        组装载重传感器报文
        :param id: 传感器id（70,71,对应112,113）
        :param sign:重要数据标识0-普通，1-重要
        :param dw:重量单位，单位：0-0.1Kg；1-1kg；2-10kg；3-100kg；4-255 保留
        :param zt:载重状态，01-空载； 02-满载； 03-超载； 04-装载； 05-卸载；06-轻载；07-重载
        :param cs:装载次数0-255
        :param zl:载荷重量
        :param zzzl:装载卸载重量
        :param ad1:ad值
        :param ad2:原始ad值
        :param ad3:浮动零点
        :return:
        '''
        data=jctool.to_hex(id,2)+"18"+jctool.to_hex(sign,4)+jctool.to_hex(dw,2)+jctool.to_hex(zt,2)+"0000"+jctool.to_hex(cs,4)+"0000"+jctool.to_hex(zl,4)+jctool.to_hex(zzzl,4)+jctool.to_hex(ad1,4)+"0000"+jctool.to_hex(ad2,4)+"0000"+jctool.to_hex(ad3,4)
        return data

    def add_gs(self,id,fs,zt,ztime,bd,sj):
        '''
        组装工时传感器数据
        :param id:工时传感器id（80,81,对应128,129）
        :param fs:工时检测方式（0-电压，1-油耗阈值，2-油耗波动）
        :param zt:工作状态（0-停机，1-工作）
        :param ztime:当前状态持续时长s
        :param bd:波动值（0.1v或0.01L/h）
        :param sj:工时数据（0.1V或0.01L/H）
        :return:工时传感器数据
        '''
        data=jctool.to_hex(id,2)+"0C"+jctool.to_hex(fs,4)+jctool.to_hex(zt,4)+jctool.to_hex(ztime,8)+jctool.to_hex(bd,4)+jctool.to_hex(sj,4)
        return data

    def add_zio(self,k0,k1,k2,k3):
        '''自带io
        获取自带开关状态，最多4个（0-断开，1-闭合，2-无接口）
        :param k0:
        :param k1:
        :param k2:
        :param k3:
        :return:自带io报文
        '''
        data="9004"+jctool.to_hex(k0,2)+jctool.to_hex(k1,2)+jctool.to_hex(k2,2)+jctool.to_hex(k3,2)
        return data

    def add_wio(self,sign,m,zt,yzt):
        """拓展io"""
        n=(int(m+32)/32)+1
        a=4*n*2
        da=jctool.to_hex(sign,2)+jctool.to_hex(m,2)+"00"+jctool.to_hex(n,2)+jctool.to_hex(zt,a)
        len=len(da)/2+1
        data="id"+jctool.to_hex(len,2)+da
        return data
    def gzm(self,id,value):
        data=str(id)+str(binascii.b2a_hex(value))
        return jctool.change_a(data)

    def obd_drive_start(self,driving_order,start_time):
        """OBD行程开始信息,OBD的f3id为a0
        行程序号（8）+开始时间（8）
        """
        driving_msg="a00901"+jctool.to_hex(driving_order,8)+jctool.to_hex(start_time,8)
        return driving_msg

    def obd_drive_else(self,driving_stage,driving_order,start_time,end_time,driving_time,driving_on_time,
                       driving_meliage,idling_times,idling_time,oilcost,driving_oilcost,idling_oilcost,
                       speed_up_times,speed_down_times,swerve_times,brake_times,separation_and_reuniontimes):

        """OBD行程进行结束信息
        数据长度（2）+ 行程阶段（2）+行程序号（8）+开始时间（8）+结束时间（8）+行程时长（6）+
        行程内行驶时长（6）+行程内行驶里程（8）+行程内怠速次数+（4）+行程内怠速时长（6）+
        行程总油耗（8）+行程内行驶油耗（8）+行程内怠速油耗（8）+行程内急加速次数（4）+行程内急减速次数（4）
        行程内急转弯次数（4）+行程内刹车次数（4）+行程内离合次数（4）+保留（6）
        """
        driving_meliage=int(driving_meliage*100)
        oilcost=int(oilcost*100)
        driving_oilcost=int(driving_oilcost*100)
        idling_oilcost=int(idling_oilcost*100)
        driving_msg=jctool.to_hex(driving_stage,2)+jctool.to_hex(driving_order,8)+jctool.to_hex(start_time,8)+\
                    jctool.to_hex(end_time,8)+jctool.to_hex(driving_time,6)+jctool.to_hex(driving_on_time,6)+\
                    jctool.to_hex(driving_meliage,8)+jctool.to_hex(idling_times,4)+jctool.to_hex(idling_time,6)+\
                    jctool.to_hex(oilcost,8)+jctool.to_hex(driving_oilcost,8)+jctool.to_hex(idling_oilcost,8)+\
                    jctool.to_hex(speed_up_times,4)+jctool.to_hex(speed_down_times,4)+jctool.to_hex(swerve_times,4)+\
                    jctool.to_hex(brake_times,4)+jctool.to_hex(separation_and_reuniontimes,4)+"000000000000"
        driving_msg="a0"+jctool.to_hex(len(driving_msg)/2,2)+driving_msg
        return driving_msg

    def add_ty(self):
        # 胎压(未实现，没有好方案定义各轮胎参数，参数也太多)
        pass



    def send_3(self, ip, port, zc, jq, gps):
        '''
        按照顺序发送3组报文
        :param ip:
        :param port:
        :param zc:
        :param jq:
        :param gps:
        :return:
        '''
        HOST = str(ip)
        PORT = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.settimeout(10)
        s.send(jctool.to_pack(zc))
        time.sleep(5)
        s.send(jctool.to_pack(jq))
        time.sleep(5)
        for i in range(0, 5):
            s.send(jctool.to_pack(gps))
            time.sleep(10)
        s.close()
        time.sleep(3)

    def send_1(self, ip, port, bw):
        '''
        重复发送一组报文(字符串)
        :param ip:
        :param port:
        :param bw:
        :return:
        '''

        HOST = str(ip)
        PORT = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.settimeout(10)
        s.send(bw)
        time.sleep(3)
        for i in range(0, 5):
            s.send(bw)
            time.sleep(10)
        s.close()
        time.sleep(3)

    def send_udp(self, ip, port, bw):
        '''
        以udp协议发送字符串
        :param ip:
        :param port:
        :param bw:
        :return:
        '''
        HOST = str(ip)
        PORT = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(1, 5):
            s.sendto(jctool.to_pack(bw), (HOST, PORT))
            time.sleep(10)
        s.close()
        time.sleep(3)

    def load_parameter(self, name, path):
        """读取参数，参数名+路径"""
        str = open(path, 'r')
        j = str.read()
        str.close()
        dict = eval(j)
        parameter = dict.get(name)
        return parameter

    def c_cd(self, sendtime, senddevice, str1):
        """构建f3超待协议报文"""
        senddevice = str(senddevice)
        s = self.change_b(str1)
        while len(senddevice) < 12:
            senddevice = "0" + senddevice
        data = s[2:10] + senddevice + s[22:70] + str(sendtime) + s[76:-4]
        jy = self.get_jiaoyan(data)
        bw = "7e" + data + jy + "7e"
        return bw

    def c_aso(self, sendtime, senddevice, str1):
        senddevice = str(senddevice)
        s = self.change_b(str1)
        print "s=" + s
        while len(senddevice) < 12:
            senddevice = "0" + senddevice
        data = s[2:10] + str(senddevice) + s[22:70] + str(sendtime) + s[82:-4]
        bw = jctool.add_all(data)
        return bw


