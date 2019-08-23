# -*- coding: utf-8 -*-
# 本文件存放基础方法
import socket
import datetime
import binascii
import struct
import time

class jctool(object):
    def __init__(self):
        pass
    def to_hex(self, str_10, num):
        '''
        把十进制数字转化为16进制，并按照传入位数前面补0
        :param str_10: 十进制数
        :param num: 位数（不足+0，超过未处理）
        :return:
        '''
        s = str(hex(int(str_10)))   #转换为16进制
        s = s[2:]  #去掉0x
        while len(s) < num:  #不足位数前面补0
            s = "0" + s
        if  len(s) > num:
            print (str(str_10)+u"转化指定位数超限")
            return False
        else:
            return s

    def to_int(self,str_16):
        nu=int(str_16,16)
        return nu

    def get_id(self, deviceid):
        '''
        处理设备号，转化为ascii码
        :param deviceid: s设备号，7位
        :return:
        '''
        asc_id = str(binascii.b2a_hex(str(deviceid)))  #deviceid ASCII编码 以十六进制表示
        # if len(asc_id)<> 14:
        #     print u"设备号格式有误"+asc_id
        return asc_id


    def get_vnum(self, ver):
        '''
        处理车牌号,gbk编码后转ascii码
        :param ver: 车牌号，7位
        :return:
        '''
        g = str(ver)
        g1 = g.decode('utf-8').encode('gbk')
        g2 = binascii.b2a_hex(g1)
        if len(g2) <> 16:
            print u"车牌号格式错误"
        return str(g2)
    def character_string(self, param,length=0):
        '''
        处理字符串字段,gbk编码后转ascii码
        :param param: 编码前的汉字
        :param length: 编码后的长度范围，无要求传入0
        :return:编码后的字符串
        '''
        g = str(param)
        g1 = g.decode('utf-8').encode('gbk')
        g2 = binascii.b2a_hex(g1)
        while len(g2) < length:
            g2 = g2+"30"
        return str(g2)
    # 关闭tcp连接
    def close(self, tcplink):
        tcplink.close()
    #把报文转化为大写，每两个字符后加空格,最后无空格
    def change_a(self, st):
        st = str(st)
        a = ""
        while st:
            if len(st)==2:
                a = a + st[0:2].upper()
                st=""
            else:
                a = a + st[0:2].upper() + " "
                st = st[2:]
        return a

    def change_b(self, str):
        str = str
        a = ""
        while str:
            a = a + str[0:2].lower()
            str = str[3:]
        return a

    def de(self, st):
        # 处理7d7e，添加包头包尾
        da=""
        while st:
            s=st[0:2]+" "
            st=st[2:]
            da=da+s.upper()
        da=da.replace("7D","7D 01").replace("7E","7D 02")
        da=("7E"+da+"7E").replace(" ","")
        return da


    def dd(self, st):
        # 处理响应中的7D01和7d02,并大写转化
        da=""
        while st:
            s=st[0:2]+" "
            st=st[2:]
            da=da+s.upper()
        da=da.replace("7D 02","7E").replace("7D 01","7D").replace(" ","")
        return da

    # 组包发送报文
    def send_data(self, tcplink, data):
        print (time.strftime("%y-%m-%d %H:%M:%S ", time.localtime())+"--发送报文： "+self.change_a(data))
        tcplink.send(self.to_pack(data))
        return self.change_a(data)
    #打包数据
    def to_pack(self,data):
        '''
        接收组装好的16进制字符串，进行打包返回数据包\n
        data: 16进制字符串\n
        return:数据包
        '''
        str1 = ''
        str2 = ''
        data=str(data)
        while data:
            str1=data[0:2]
            s=int(str1,16) #str1是一个16进制的数，int()函数将其用十进制数表示
            str2+=struct.pack('B',s)#B表示类型格式unsigned char
            data=data[2:]
        return str2
    # 接收报文
    def receive_data(self, tcplink):
        res = tcplink.recv(1024)
        res =res.encode('hex')#将res（unicode）编码成16进制的str对象;python内部表示字符串用unicode，和人交互的时候用str对象;
        print (time.strftime("%y-%m-%d %H:%M:%S ", time.localtime())+"--接收报文： "+self.change_a(res))
        return res

    # 建立tcp连接
    def tcp_link(self, HOST, PORT):
        HOST = str(HOST)
        PORT = int(PORT)
        tcplink = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        tcplink.connect((HOST, PORT))
        tcplink.settimeout(10)
        return tcplink

    # 生成校验码，转化7d7e，添加包头包尾
    def add_all(self, datastr):
        po = str(datastr)
        add = int(po[0:2], 16)
        po = po[2:]
        while len(po):#生成校验码
            add = add ^ int(po[0:2], 16)
            po = po[2:]
        if add >= 16:
            jy = hex(add)[-2:]
        elif add == 0:
            jy = "00"
        else:
            jym = hex(add)[-1:]
            jy = "0" + str(jym)
        data=datastr+jy
        data=self.de(data) #转化7d7e,添加包头包尾
        return data

    #时间%y%m%d%H%M%S转化为时间戳
    def ttos(self,sendtime):
        timeArray = time.strptime(str(sendtime), "%y%m%d%H%M%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    #时间戳转化为北京时间%y%m%d%H%M%S
    def stot(self,timestamp):
        timestamp=timestamp+28800
        dateArray = datetime.datetime.utcfromtimestamp(timestamp)
        otherStyleTime = dateArray.strftime("%y%m%d%H%M%S")
        return str(otherStyleTime)

