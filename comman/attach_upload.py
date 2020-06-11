#coding=utf-8
from testlibrary import jctool
import time
import threading
import socket
import os
import struct



def attach_upload(tp,res,mobile,version):
    if version == 1:
        while len(mobile) < 20:
            mobile = '0' + mobile
        # iplenth = (int(res[36:38],16))*2 #获取9208指令中服务器地址长度字段
        ip2 = "112.126.64.32"
        port2 = 7900
        alarmflag = res[66:108]  # 获取报警标识号
        alarm_number = res[108:172]
        # 文件名（00_e1_e100_0_b87441129fb34ef8969fd0de2739d15e.jpg）转成16进制格式

        filepath = 'C:\\Users\\zwkj\\Desktop\\00_E1_E100_0_b87441129fb34ef8969fd0de2739d15e.jpg'
        filename1 = os.path.basename(filepath)
        filename = tp.character_string(filename1)
        filename2 = tp.character_string(filename1,50)
        filesize = os.stat(filepath).st_size
        filesize1 = tp.to_hex(filesize,8)
        # filename = '30305F65315F653130305F305F62383734343131323966623334656638393639666430646532373339643135652E6A7067'

        filenamelen = str(hex(len(filename) / 2))[2:]  # 文件名长度

        attachlist = filenamelen + filename + '00' + '000044EA'  # 组装附件信息内容
        usual_body = mobile + alarmflag + alarm_number + '00' + '01' + attachlist  # 组装1210指令消息体
        head = tp.data_head(mobile, 4624, usual_body, 5, version)
        redata = tp.add_all(head + usual_body)

        link1 = tp.tcp_link(ip2, port2)
        tp.send_data(link1,redata)
        # tp.receive_data(link1)
        time.sleep(10)
        # 1211指令的消息体跟附件信息内容一样
        fileinfo_head = tp.data_head(mobile, 4625, attachlist, 5, version)
        fileinfo = tp.add_all(fileinfo_head + attachlist)
        tp.send_data(link1, fileinfo)

        streamhead = bytearray(b'\x30\x31\x63\x64')
        fhead = struct.pack('128sl',filename1,filesize)
        data = streamhead + fhead
        link1.send(data)
        picdata = open(filepath, 'rb')
        while 1:
            picbytes = picdata.read(1024)
            link1.send(picbytes)


        tp.close(link1)







        # 读取图片文件并发送码流:帧头+文件名称【50】+数据偏移量【4】+数据长度【4】+数据体长度【4】
        # streamhead = bytearray(b'\x30\x31\x63\x64')
    #     streamhead ='30316364'
    #     while len(filename) < 100:
    #         filename = '0' + filename
    #     # filename1 = bytes(filename)
    #     i = 1
    #     picdata = open('C:\\Users\\zwkj\\Desktop\\00_E1_E100_0_b87441129fb34ef8969fd0de2739d15e.jpg', 'rb')
    #     picbytes = picdata.read()
    #     picsize = len(picbytes)
    #     filesize = tp.to_hex(picsize,4)
    #     n = picsize % 65535
    #     while (n-i) == 0:
    #         dataoffset = '00000000'
    #         dataoffset = bytearray.fromhex(dataoffset)
    #         # datasize = bytearray.fromhex(tp.to_hex(picsize,4))
    #         datastream = streamhead + filename + dataoffset + filesize + filesize
    #         print datastream
    #         datastream = tp.to_pack(datastream)
    #         link1.send(datastream)
    #         picstream = picdata.read(picsize)
    #         link1.send(picstream)
    #     while (n-i)>= 0:
    #         dataoffset = (i-1)*65535
    #         dataoffset = bytearray.fromhex(tp.to_hex(dataoffset,4))
    #         datasize = picsize - (i-1)*65535
    #         datasize = bytearray.fromhex(tp.to_hex(datasize,4))
    #         datastream = streamhead +filename + dataoffset +filesize +datasize
    #         datastream = tp.to_pack(datastream)
    #         print datastream
    #
    #         link1.send(datastream)
    #         picstream = picdata.read(65535)
    #         link1.send(picstream)
    #         i += 1
    #
    #     tp.close(link1)
    # elif version == 0:
    #     ip2 = "192.168.24.142"
    #     port2 = 7900
    #     alarmflag = "30303030303030303031E100200529172333010100"
    #     alarm_number = "3532303365633864386633353434303739653166623265396530346139393339"
    #     filename = '30305F65315F653130305F305F62383734343131323966623334656638393639666430646532373339643135652E6A7067'
    #     filenamelen = str(hex(len(filename) / 2))[2:]
    #     attachlist = filenamelen + filename + '00' + '000044EA'
    #     usual_body = "mobile" + alarmflag + alarm_number + '00' + '01' + attachlist
    #     head = tp.data_head(mobile, 4624, usual_body, 5, version)
    #     redata = tp.add_all(head + usual_body)
    #     link1 = tp.tcp_link(ip2, port2)
    #     jctool.send_data(link1, redata)
