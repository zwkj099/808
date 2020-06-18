#coding=utf-8
from testlibrary import jctool
import time
import threading
import socket
import os
import struct

'''
1、目前文件名是写死的，对应的是前向碰撞报警的文件名称
2、支持中位协议
3、使用前需要配置图片路径
'''

def attach_upload(tp,res,mobile,attach,filepath,version):
    if version == 1:
        while len(mobile) < 20:
            mobile = '0' + mobile
        iplenth = (int(res[36:38],16))*2 #获取9208指令中服务器地址长度字段
        ip2 = "112.126.64.32"
        # ip2 = "192.168.24.142"
        port2 = 7901
        alarmflag = res[42+iplenth:84+iplenth]  # 获取报警标识号
        alarm_number = res[84+iplenth:148+iplenth]
        # 文件名（00_e1_e100_0_b87441129fb34ef8969fd0de2739d15e.jpg）转成16进制格式
        #文件名称可修改，文件大小不要大于64kb
        # filepath = 'C:\\Users\\zwkj\\Desktop\\00_E1_E100_0_b87441129fb34ef8969fd0de2739d1330.jpg'
        # filepath = 'C:\\Users\\zwkj\\Desktop\\00_E1_E100_0_b87441129fb34ef8969fd0de2739d1322.mp4'
        #filename1为原始文件名，filename转为16进制后的名称
        filename1 = os.path.basename(filepath)
        filename = tp.character_string(filename1)
        filename2 = tp.character_string1(filename1,100)
        #filesize文件大小，filesize1文件大小转为16进制
        filesize = os.stat(filepath).st_size
        filesize1 = tp.to_hex(filesize,8)

        filenamelen = str(hex(len(filename) / 2))[2:]  # 文件名长度

        # attachlist = filenamelen + filename + '00' + filesize1  # 组装附件信息内容图片
        attachlist = filenamelen + filename + attach + filesize1
        usual_body = mobile + alarmflag + alarm_number + '00' + '01' + attachlist  # 组装1210指令消息体
        head = tp.data_head(mobile, 4624, usual_body, 5, version)
        redata = tp.add_all(head + usual_body)

        link1 = tp.tcp_link(ip2, port2)
        tp.send_data(link1,redata)
        tp.receive_data(link1)
        # 1211指令的消息体跟附件信息内容一样
        fileinfo_head = tp.data_head(mobile, 4625, attachlist, 5, version)
        fileinfo = tp.add_all(fileinfo_head + attachlist)
        tp.send_data(link1, fileinfo)
        tp.receive_data(link1)


        i = 0
        m = int(filesize // 65536)
        n = int(filesize % 65536)
        nsize = tp.to_hex(n,8)
        picdata = open(filepath, 'rb')
        picbytes = picdata.read()

        streamhead = '30316364'
        if m == 0:
            data1 = streamhead + filename2 + '00000000' + filesize1
            data2 = tp.to_pack(data1)
            data = data2 + picbytes
            link1.send(data)
        else:
            for i in range(m+1):
                dataoffset1 = i * 65536
                dataoffset2 = tp.to_hex(dataoffset1, 8)
                if m - i == 0:
                    # picdata.seek(dataoffset1,1)
                    data1 = streamhead + filename2 + dataoffset2 + nsize
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + filesize]
                    link1.send(data)
                    break
                elif m - i > 0:
                    data1 = streamhead + filename2 + dataoffset2 + '00010000'
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + 65536]
                    link1.send(data)
                    i += 1


        #文件上传完整指令1212
        # usual_body = filenamelen + filename + '00' + filesize1  #图片
        usual_body = filenamelen + filename + attach + filesize1
        head = tp.data_head(mobile, 4626, usual_body, 5, version)
        flishdata = tp .add_all(head + usual_body)
        tp.send_data(link1,flishdata)
        tp.receive_data(link1)


        tp.close(link1)

