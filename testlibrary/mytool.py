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
    def data_head(self, mobile, newid, data, xulie=1,version=0,num1=0,totalpack=0):
        '''
        组装消息头
        :param mobile: 手机号
        :param newid:消息id，如0100,0200
        :param data:消息体，包括基本信息，附加信息，f3信息
        :param xulie:消息流水号，默认0000
        :param version:协议版本，１表示808-2019，０表示808-2013
        :param num1:第几个分包
        :param totalpack:分包总数
        :return:对应消息id的消息头信息

        '''
        lenth = len(data) / 2
        num = num1+1
        if version==0:
            while len(mobile) < 12:
                mobile = "0" + mobile
            if totalpack==0:
                head = jctool.to_hex(newid,4) + jctool.to_hex(lenth, 4) + str(mobile) + jctool.to_hex(xulie, 4)
            else:##如果分包数不为0
                lenth = lenth + 8192  # 加上分包位的值，13位为1
                head = jctool.to_hex(newid, 4) + jctool.to_hex(lenth, 4) + str(mobile) + jctool.to_hex(xulie,4) + jctool.to_hex(totalpack, 4) + jctool.to_hex(num, 4)
        elif version==1:
            while len(mobile) < 20:
                mobile = "0" + mobile
            if totalpack == 0:
                head = jctool.to_hex(newid, 4) + jctool.to_hex(4, 1) + jctool.to_hex(lenth, 3) + jctool.to_hex(version,2) + str(mobile) + jctool.to_hex(xulie, 4)
            else:
                lenth = lenth + 24576  # 加上分包位的值　14、13位为1
                head = jctool.to_hex(newid, 4) + jctool.to_hex(lenth, 4) + jctool.to_hex(version, 2) + str(mobile) + jctool.to_hex(xulie, 4) + jctool.to_hex(totalpack, 4) + jctool.to_hex(num, 4)
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

    def zd_body(self,ids=None, pdict=None,sichuandict=None,deviceid=None,port=6975,ti=0):
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
        # sign, event, level, deviate, road_sign, fatigue,jin, wei, high, speed, zstatus, deviceid,attach_Count,port,tire_num,tire_loc,tire_alarm_type=zds


        for id in ids:
            if id in (100,101,102,103,112,113):
                # body = self.add_zdaq(id, sign, event, level, deviate, road_sign, fatigue, jin, wei, high, speed, zstatus,deviceid,attach_Count,port,tire_num,tire_loc,tire_alarm_type)
                body = self.add_zdaq(id, pdict,sichuandict,deviceid,port)
                ZDAQ_body += body
            elif id in (225,226,227,228,229,231):
                body = self.add_ZW_zdaq(id)#zdaq(id, pdict, sichuandict, deviceid, port)
                ZDAQ_body += body
            else:
                print "无主动安全数据"
        return ZDAQ_body

    # def f3_attach(self,ids=None, oils=None, wds=None, sds=None, yhs=None, zfs=None, zzs=None, gss=None, lcs=None,base=None,wifi=None,lys=None):
    def f3_attach(self,ids=None, pdict=None, sensordict=None,bluetoothdict=None):
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
        """数据格式：附加消息ID（b)+附加信息长度(b)+外设传感器总数(b)+  外设ID1(b)+外设消息长度(b)+外设消息内容(bn)+外设ID2(b)......  ;附加消息ID:如F3"""

        data = ""
        data0 = ""
        f3_data = ""
        c=3
        cont = 0#用来计算上传的传感器个数
        for i in ids:
            if i in (33,34,35,36,37):# 温度
                data0 = self.add_wd(i, sensordict['sign'], sensordict['temp'], sensordict['times'], sensordict['warn']) # 温度传感器参数
            elif i in (38,39,40,41):# 湿度
                data0 = self.add_sd(i, sensordict['sign'],sensordict['hum'],sensordict['times'],sensordict['warn'])
            elif i in (65,66,67,68):# 油量、液位
                data0 = self.add_yw(i, sensordict['oil_sign'], sensordict['AD'], sensordict['liquid_temp'], sensordict['env_temp'], sensordict[
                    'addoil'], sensordict['spilloil'], sensordict['Oil'],0, pdict['high'])
            elif i in (69,70):# 油耗
                data0 = self.add_yh(i, sensordict['oilsp'],sensordict['oiltemp'],sensordict['tio'],sensordict['times'])
            elif i == 79:  # 4Ｆ电量检测
                data0 = self.add_dljc(i, sensordict['data_id'],sensordict['alarm_id'],sensordict['terminal_power'],\
                                      sensordict['traffic_volume'],sensordict['refrigerated_capacity'],sensordict['communication_type'],sensordict['operator'])
            elif i == 80:  # 终端信息检测
                data0 = self.add_zdjc(i,sensordict['alarm_id'],sensordict['vehicle_status'], 0, 0)
            elif i == 81:  # 正反转
                data0 = self.add_zf(i, sensordict['sign'],sensordict['zts'],sensordict['fx'],sensordict['xs'],sensordict['times'],sensordict['li'],sensordict['xtimes'])
            elif i == 83:  # 里程
                data0 = self.add_lc(i, sensordict['mel'],sensordict['speed'])
            elif i == 84:  # 蓝牙信标
                data0 = self.add_ly(i, bluetoothdict['num'],bluetoothdict['UUID'],bluetoothdict['signal'],bluetoothdict['distance'],bluetoothdict['battery'])
            elif i in (112,113):#载重
                data0 = self.add_zz(i, sensordict['sign'],sensordict['dw'],sensordict['zt'],sensordict['cs'],sensordict['zl'],sensordict['zzzl'],\
               sensordict['ad1'],sensordict['ad2'],sensordict['ad3'],sensordict['datalen'])
            elif i in (128,129):# 工时
                data0 = self.add_gs(i, sensordict['fs'],sensordict['ztt'],sensordict['ztime'],sensordict['bd'],sensordict['sj'],sensordict['gslen'])

            #判断长度是否超过255，超过则分开组装，将data0赋值到下一轮组装数据中
            if (len(data0 + data) / 2 + 1) < 255:
                data += data0
                cont = cont + 1
            else:
                f3_data += self.add_f3_data(cont, data, c)
                data = data0
                cont = 1
                c += 1

        # 处理基站和wifi数据
        if ids.__contains__(8)==True and ids.__contains__(9)==False:
            #组装基站
            data0 = self.add_base(8,sensordict['basever'], sensordict['report_frequency'], sensordict['position_mode'],
                    sensordict['time_num'], sensordict['start_time'], sensordict['info_status'], \
                    sensordict['info_groupnum'], sensordict['mcc'], sensordict['sid'], sensordict['lac_nid'],
                    sensordict['cell_bid'], sensordict['bcch'], sensordict['bsic'], sensordict['dbm'], \
                    sensordict['c1'], sensordict['c2'], sensordict['txp'], sensordict['rla'], sensordict['tch'],
                    sensordict['ta'], sensordict['rxq_sub'], sensordict['rxq_full'])
            if (len(data0 + data) / 2 + 1) < 255:
                data += data0
                cont = cont + 1
            else:
                f3_data += self.add_f3_data(cont, data, c)
                data = data0
                cont = 1
                c += 1
        elif ids.__contains__(8)==True and ids.__contains__(9)==True:
            #组装基站和wifi,要上传wifi数据，必须要同时上传基站数据
            data0 = self.add_base(8,sensordict['basever'], sensordict['report_frequency'], sensordict['position_mode'],
                    sensordict['time_num'], sensordict['start_time'], sensordict['info_status'], \
                    sensordict['info_groupnum'], sensordict['mcc'], sensordict['sid'], sensordict['lac_nid'],
                    sensordict['cell_bid'], sensordict['bcch'], sensordict['bsic'], sensordict['dbm'], \
                    sensordict['c1'], sensordict['c2'], sensordict['txp'], sensordict['rla'], sensordict['tch'],
                    sensordict['ta'], sensordict['rxq_sub'], sensordict['rxq_full'])
            if (len(data0 + data) / 2 + 1) < 255:
                data += data0
                cont = cont + 1
            else:
                f3_data += self.add_f3_data(cont, data, c)
                data = data0
                cont = 1
                c += 1

            data0 = self.add_wifi(9,sensordict['ver'], sensordict['softver'], sensordict['electric'], sensordict['csq'],
                    sensordict['groupnum'], sensordict['mac'], sensordict['wifi_sign'])
            if (len(data0 + data) / 2 + 1) < 255:
                data += data0
                cont = cont + 1
            else:
                f3_data += self.add_f3_data(cont, data, c)
                data = data0
                cont = 1
                c += 1
        f3_data +=self.add_f3_data(cont, data,c)
        return f3_data

    def add_base(self,id,basever,report_frequency,position_mode,time_num,start_time,info_status,info_groupnum,mcc,sid,lac_nid,cell_bid,bcch,bsic,dbm,c1,c2,txp,rla,tch,ta,rxq_sub,rxq_full):
        data = jctool.to_hex(id, 2) + "24" + jctool.to_hex(basever, 2) + jctool.to_hex(report_frequency,8) + jctool.to_hex(position_mode, 2) + \
               jctool.to_hex(time_num, 2) + str(int(start_time)) + jctool.to_hex(info_status, 2) + jctool.to_hex(info_groupnum, 2) + \
               jctool.to_hex(mcc, 4) + jctool.to_hex(sid, 4) + jctool.to_hex(lac_nid, 4) + jctool.to_hex(cell_bid, 4) + jctool.to_hex(bcch, 4) + \
               jctool.to_hex(bsic, 4) + jctool.to_hex(dbm, 2) + jctool.to_hex(c1, 4) + jctool.to_hex(c2,4) + jctool.to_hex(txp, 2) + \
               jctool.to_hex(rla, 2) + jctool.to_hex(tch, 4) + jctool.to_hex(ta, 2) + jctool.to_hex(rxq_sub,2) + jctool.to_hex(rxq_full, 2)
        # print data
        return data
    
    def add_wifi(self,id,ver,softver,electric,csq,groupnum,mac,wifi_sign):
        # 13代表数据长度，16进制
        mac ='010082400000'
        wifi_sign =0
        csq = 31
        data = jctool.to_hex(id, 2) + "13" + jctool.to_hex(ver, 2) + jctool.to_hex(softver,16) + jctool.to_hex(electric, 2) + \
               jctool.to_hex(csq, 2) + jctool.to_hex(groupnum, 2) + str(mac) + jctool.to_hex(wifi_sign, 2)

        #     data=hexcovert.to_hex(id,2)+"0C"+hexcovert.to_hex(ver,2)+hexcovert.to_hex(softver,16)+hexcovert.to_hex(electric,2)+\
        #          hexcovert.to_hex(csq,2)+hexcovert.to_hex(grouopnum,2)
        # print mac
        # print data
        return data

    # def add_zdaq(self,id,sign,event,level,deviate,road_sign,fatigue,jin, wei, high, speed,zstatus,deviceid,attach_Count,port=6975,tire_num=0,tire_loc=0,tire_alarm_type=40,tire_pressure=3,tire_temp=35,tire_electric=50):
    def add_zdaq(self, id, pdict,sichuandict,deviceid,port,tire_pressure=3,tire_temp=35,tire_electric=50,mobile='00000000013300000048'):
        ''' 川冀标主动安全数据
        :param id: 外设ID（100、101、102、103、112、113）
        :param port:监控对象协议对应端口号
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
        :param tire_num ：胎压报警/事件列表总数
        :param tire_loc: 报警轮胎位置
        :param tire_alarm_type：胎压报警/事件类型,2：胎压过高，4：胎压过低，8：胎温过高，16：传感器异常，32：胎压不平衡，64：慢漏气，128：电池电量低
        :param tire_pressure :胎压
        :param tire_temp :胎温
        :param tire_electric:电池电量

        '''

        jin = float( pdict['jin']) * 1000000
        wei = float(pdict['wei']) * 1000000
        ti = time.strftime("%y%m%d%H%M%S", time.localtime())
        # date = datetime.datetime.strptime('2019-08-08 09:00:00', "%Y-%m-%d %H:%M:%S")
        # ti = date.strftime("%y%m%d%H%M%S")
        alarm= jctool.get_id(deviceid)+str(ti)+"00"+jctool.to_hex(sichuandict['attach_Count'], 2)+"00"
        data0=jctool.to_hex(pdict['speed'], 2) + jctool.to_hex(pdict['high'], 4) + jctool.to_hex(wei, 8) + jctool.to_hex(jin, 8) + str(ti) + jctool.to_hex(sichuandict['zstatus'],4) + alarm
        tire_alarm_info = jctool.to_hex(sichuandict['tire_num'],2)+""
        alarmID="00000001"#报警ＩＤ（DWORD)
        # 驾驶辅助功能报警信息
        if id==100:
            data = alarmID+jctool.to_hex(sichuandict['sign'], 2)+jctool.to_hex(sichuandict['event'], 2)+ jctool.to_hex(sichuandict['level'], 2) + jctool.to_hex(pdict['speed'], 2) + "09"+jctool.to_hex(sichuandict['deviate'], 2)\
                   + jctool.to_hex(sichuandict['road_sign'], 2)+"00" + data0
        # 驾驶员行为监测功能报警信息
        elif id==101:
            data = alarmID+jctool.to_hex(sichuandict['sign'], 2)+jctool.to_hex(sichuandict['event'], 2)+ jctool.to_hex(sichuandict['level'], 2)+jctool.to_hex(sichuandict['fatigue'], 2) + "00000000" + data0
        # 激烈驾驶报警信息
        elif id==112:
            data = alarmID+jctool.to_hex(sichuandict['sign'], 2)+jctool.to_hex(sichuandict['event'], 2)+ "0009" + "0008" + "0008"+ data0
        # 轮胎状态监测报警信息
        elif id==102:
            if port==6998: #浙标中盲区监测对应外设ID为66
                data = alarmID + jctool.to_hex(sichuandict['sign'],2)+jctool.to_hex(sichuandict['event'],2)+data0
            else:
                while sichuandict['tire_num']>0:
                    tire_alarm_info += jctool.to_hex(sichuandict['tire_loc'], 2) + jctool.to_hex(sichuandict['tire_alarm_type'],4) + jctool.to_hex(tire_pressure, 4) + jctool.to_hex(tire_temp, 4) + jctool.to_hex(tire_electric, 4)
                    sichuandict['tire_loc'] += 1
                    sichuandict['tire_num'] -= 1
                data = alarmID + jctool.to_hex(sichuandict['sign'],2) + data0 + tire_alarm_info

        # 盲区监测报警信息
        elif id==103:
            data = alarmID + jctool.to_hex(sichuandict['sign'],2)+jctool.to_hex(sichuandict['event'],2)+data0
        # 卫星定位系统报警信息
        elif id==113:
            data = alarmID+"0001000900" + data0
        #不按规定上下客及超员检测报警信息
        elif id==104:
            data = alarmID + jctool.to_hex(sichuandict['sign'], 2) + jctool.to_hex(sichuandict['event'],2) + jctool.to_hex(sichuandict['level'], 2) + "0000000000" + data0
        else:
            print "无主动安全数据",id
            data=""
        lent = len(data) / 2 + 1
        # 组装为信息并返回
        zddata = jctool.to_hex(id, 2) + jctool.to_hex(lent, 2) + data
        return zddata

    def add_ZW_zdaq(self, id,mobile='00000000013300000048'):# pdict, sichuandict, deviceid, port, tire_pressure=3, tire_temp=35, tire_electric=50,):
        alarmID = "00000001"  # 报警ＩＤ（DWORD)
        alarmType = ['00000001','00000002','00000004','00000008','00000016','00000032','00000064','00000128','00000256','00000512','00131072','00262144']
        alarmTypeb = ['E100','E101','E102','E103','E104','E105','E106','E107','E108','E109','E117','E118']
        alarmType1 = ['00000001','00000002','00000004','00000008','00000016','00000032','00000064','00000128','00131072','00262144','00524288']
        alarmTypeb1 = ['E200','E201','E202','E203','E204','E205','E206','E207','E217','E218','E219']
        alarmType2 = ['0001','0002','0004']
        alarmTypeb2 = ['E400','E401','E402']
        alarmTypeb3 = ['01','02','04','08','16','32','64']
        ti = time.strftime("%y%m%d%H%M%S", time.localtime())
        if id==225:#前向监测系统,225-231
            # i = random.randint(0,11)
            data = alarmID + alarmType[0] + "020202020201"+mobile+ alarmTypeb[0] + ti +"010100"
        elif id==226:#前向监测系统
            j = random.randint(0,10)
            data = alarmID +alarmType1[j] + "020201"+mobile+alarmTypeb1[j]+ ti +"010100"
        elif id == 227:  # 轮胎气压监测系
            m = random.randint(0,6)
            data = "01000001" + "00" + alarmTypeb3[m]+ "000100020200"
        elif id == 228:  # 盲区监测系统
            k = random.randint(0,2)
            data = alarmType2[k]+"01" + mobile + alarmTypeb2[k] + ti + "010100"
        elif id == 229:  #原车数据;      正常情况下只用0xE5，如果数据字节数超过255个字节，则后续数据流值放在附加信息0xE6中(229-230)
            data = "0001"+"0647"+"01"
        elif id == 231:  # 终端分析上报
            data = "0178776500000000"
        else:
            print "无中位标准主动安全数据",id
            data=""
        lent = len(data) / 2
        # 组装为信息并返回
        ZW_zddata = jctool.to_hex(id, 2) + jctool.to_hex(lent, 2) + data
        return ZW_zddata
    def extra_info(self, ids=None, ex808dict=None): #vedio_alarm=0, vedio_signal=0, memery=0, abnormal_driving=0, meilage=0, oil=0,speed=0, by=0, wn=None):
        """# 组装附加信息"""

        data = ""
        for i in ids:
            if i == 1:
                meilage = int(float(ex808dict['mel']) * 10)  #里程，DWORD，1/10km，对应车上里程表读数
                data += self.add_additional(i, 4, meilage)
            elif i == 2:
                oil = int(float(ex808dict['oil']) * 10) #油量，WORD，1/10L，对应车上油量表读数
                data += self.add_additional(i, 2, oil)
            elif i == 3:
                speed = int(float(ex808dict['extra_speed']) * 10)#行驶记录功能获取的速度，WORD，1/10km/h
                data += self.add_additional(i, 2, speed)
            elif i == 6:
                data +=self.add_additional(i,2,ex808dict['temper']) #车箱温度
            elif i == 20:
                data += self.add_additional(i, 4, ex808dict['vedio_alarm'])# 1078协议，视频相关报警
            elif i in (21, 22):
                data += self.add_additional(i, 4, ex808dict['vedio_signal'])  # 1078协议，视频信号丢失报警状态、视频信号遮挡报警状态
            elif i == 23:
                data += self.add_additional(i, 2, ex808dict['memery'])# 1078协议，存储器故障报警状态
            elif i == 24:
                data += self.add_additional(i, 2, ex808dict['abnormal_driving'])#1078协议，异常驾驶行为报警详细描述
            elif i == 48:
                data += self.add_additional(i, 1, ex808dict['by'])#无线通信网络信号强度
            elif i == 49:
                data += self.add_additional(i, 1, ex808dict['wn'])#GNSS 定位卫星数
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

    def add_f3_data(self,num,data_body,c):
        '''组装传感器信息组合f3信息，把各个传感器信息打包成f3附加信息
        :param num:传感器数量
        :param data_body: 传感器信息body
        :param c :当Ｆ３附加消息超过255时，进行Ｆ３附加信息拆分，值从３开始依次递增
        :return: f3附加信息
        '''
        f3data=""
        if num!=0:
            lent=len(data_body)/2+1 #计算f3附加消息长度
            f3data="F" + str(c)+jctool.to_hex(lent,2)+jctool.to_hex(num,2)+data_body #组装为f3信息
        return f3data

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
        """
        13版和19版本相同：{外设ID+}　数据长度（b)+重要数据标识(b)+温度值(b3)+超出阈值持续时间(DWORD)+高低温报警(DWORD)
        """
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
        """
        13版和19版本相同：{外设ID+}　数据长度（b)+重要数据标识(b)+湿度值(b3)+超出阈值持续时间(DWORD)+湿度报警(DWORD)
        """
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
        """
        13版和19版本相同：{外设ID+}数据长度（b)+重要数据标识(b)+AD值(b3)+液体温度(DWORD)+环境温度(DWORD)+加油量(DWORD)+漏油量(DWORD)+液体量(DWORD)+液位百分比(DWORD)+液位高度(DWORD)
        """
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

    def add_zdjc(self,id,alarm_id,vehicle_status,tio,times):
        '''
        获取终端及车辆信息检测报文
        :param id: 终端信息检测id（0Ｘ50，对应80）
        :param alarm_id:报警标识
        :param vehicle_status:车辆状态
        :param tio:
        :param times:
        :return:终端及车辆信息检测报文
        '''
        data0=jctool.to_hex(alarm_id,4)+"00000111"+"00"+"00"+jctool.to_hex(vehicle_status,4)+"0011"+"0001000100010002"+"000000000000"
        size = len(data0) / 2
        data = jctool.to_hex(id, 2) +jctool.to_hex(size,2)+data0
        return data

    def add_dljc(self,id,data_id,alarm_id,terminal_power,traffic_volume,refrigerated_capacity,communication_type, operator):
        '''
        获取电量检测报文
        :param id: 终端信息检测id（0Ｘ4Ｆ，对应79）
        :param data_id:数据标识
        :param alarm_id:报警标识
        :param terminal_power:电量
        :param traffic_volume:行车电量
        :param refrigerated_capacity:冷藏电量
        :return:电量检测检测报文
        '''
        data0=jctool.to_hex(data_id,2)+jctool.to_hex(alarm_id,2)+jctool.to_hex(terminal_power,4)+jctool.to_hex(traffic_volume,4)+jctool.to_hex(refrigerated_capacity,4)+jctool.to_hex(communication_type,2)+jctool.to_hex(operator,2)+"0011"
        size = len(data0) / 2
        data = jctool.to_hex(id, 2) +jctool.to_hex(size,2)+data0
        return data

    def add_zf(self,id,sign,zts,fx,xs,times,li,xtimes):
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
        data=jctool.to_hex(id,2)+"18"+jctool.to_hex(sign,2)+jctool.to_hex(zts,6)+jctool.to_hex(fx,8)+jctool.to_hex(xs,8)+jctool.to_hex(times,8)+jctool.to_hex(li,8)+jctool.to_hex(xtimes,8)
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

    def add_zz(self,id,sign,dw,zt,cs,zl,zzzl,ad1,ad2,ad3,datalen='18'):
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
        if int(datalen)<10:
            datalen = "0"+str(int(datalen))
        else:
            datalen = str(int(datalen))
        data=jctool.to_hex(id,2)+str(datalen)+jctool.to_hex(sign,4)+jctool.to_hex(dw,2)+jctool.to_hex(zt,2)+"0000"+jctool.to_hex(cs,4)+"0000"+jctool.to_hex(zl,4)+jctool.to_hex(zzzl,4)+jctool.to_hex(ad1,4)+"0000"+jctool.to_hex(ad2,4)+"0000"+jctool.to_hex(ad3,4)
        return data

    def add_gs(self,id,fs,ztt,ztime,bd,sj,gslen='0C'):
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
        data=jctool.to_hex(id,2)+str(gslen)+jctool.to_hex(fs,4)+jctool.to_hex(ztt,4)+jctool.to_hex(ztime,8)+jctool.to_hex(bd,4)+jctool.to_hex(sj,4)
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


    def footfall_info(self,mobile,starttime,endtime,getonnum,getoffnum,version):
        """
        :param starttime:
        :param endtime:
        :param getonnum:
        :param getoffnum:
        :return:
        """
        dbody = str(starttime)+str(endtime)+jctool.to_hex(getonnum,4)+jctool.to_hex(getoffnum,4)
        hhead = self.data_head(mobile, 4101, dbody, 1, version)
        data = self.add_all(hhead + dbody)
        return data